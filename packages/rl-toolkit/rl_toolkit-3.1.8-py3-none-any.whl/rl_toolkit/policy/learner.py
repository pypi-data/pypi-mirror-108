from rl_toolkit.networks import Actor, Critic

import os
import reverb
import wandb

import tensorflow as tf


class Learner:
    """
    Learner (based on Soft Actor-Critic)
    =================
    Paper: https://arxiv.org/pdf/1812.05905.pdf
    Attributes:
        env: the instance of environment object
        max_steps (int): maximum number of interactions do in environment
        learning_starts (int): number of interactions before using policy network
        buffer_capacity (int): the capacity of experiences replay buffer
        batch_size (int): size of mini-batch used for training
        actor_learning_rate (float): learning rate for actor's optimizer
        critic_learning_rate (float): learning rate for critic's optimizer
        alpha_learning_rate (float): learning rate for alpha's optimizer
        tau (float): the soft update coefficient for target networks
        gamma (float): the discount factor
        model_a_path (str): path to the actor's model
        model_c1_path (str): path to the critic_1's model
        model_c2_path (str): path to the critic_2's model
        save_path (str): path to the models for saving
        db_path (str): path to the database
        log_wandb (bool): log into WanDB cloud
    """

    def __init__(
        self,
        # ---
        env,
        max_steps: int,
        learning_starts: int = 10000,
        # ---
        buffer_capacity: int = 1000000,
        batch_size: int = 256,
        # ---
        actor_learning_rate: float = 7.3e-4,
        critic_learning_rate: float = 7.3e-4,
        alpha_learning_rate: float = 7.3e-4,
        # ---
        update_interval: int = 64,
        # ---
        tau: float = 0.01,
        gamma: float = 0.99,
        # ---
        model_a_path: str = None,
        model_c1_path: str = None,
        model_c2_path: str = None,
        save_path: str = None,
        db_path: str = None,
        # ---
        log_wandb: bool = False,
        log_interval: int = 64,
    ):
        self._env = env
        self._max_steps = max_steps
        self._learning_starts = learning_starts
        self._update_interval = tf.constant(update_interval)
        self._gamma = tf.constant(gamma)
        self._tau = tf.constant(tau)
        self._save_path = save_path
        self._log_wandb = log_wandb
        self._log_interval = log_interval

        # init param 'alpha' - Lagrangian constraint
        self._log_alpha = tf.Variable(0.0, trainable=True, name="log_alpha")
        self._alpha = tf.Variable(0.0, trainable=False, name="alpha")
        self._alpha_optimizer = tf.keras.optimizers.Adam(
            learning_rate=alpha_learning_rate, name="alpha_optimizer"
        )
        self._target_entropy = tf.cast(
            -tf.reduce_prod(self._env.action_space.shape), dtype=tf.float32
        )

        # Actor network (for learner)
        self._actor = Actor(
            state_shape=self._env.observation_space.shape,
            action_shape=self._env.action_space.shape,
            learning_rate=actor_learning_rate,
            model_path=model_a_path,
        )

        # Critic network & target network
        self._critic_1 = Critic(
            state_shape=self._env.observation_space.shape,
            action_shape=self._env.action_space.shape,
            learning_rate=critic_learning_rate,
            model_path=model_c1_path,
        )
        self._critic_targ_1 = Critic(
            state_shape=self._env.observation_space.shape,
            action_shape=self._env.action_space.shape,
            learning_rate=critic_learning_rate,
            model_path=model_c1_path,
        )

        # Critic network & target network
        self._critic_2 = Critic(
            state_shape=self._env.observation_space.shape,
            action_shape=self._env.action_space.shape,
            learning_rate=critic_learning_rate,
            model_path=model_c2_path,
        )
        self._critic_targ_2 = Critic(
            state_shape=self._env.observation_space.shape,
            action_shape=self._env.action_space.shape,
            learning_rate=critic_learning_rate,
            model_path=model_c2_path,
        )

        # first make a hard copy
        self._update_target(self._critic_1, self._critic_targ_1, tau=tf.constant(1.0))
        self._update_target(self._critic_2, self._critic_targ_2, tau=tf.constant(1.0))

        if db_path is None:
            checkpointer = None
        else:
            checkpointer = reverb.checkpointers.DefaultCheckpointer(path=db_path)

        # actual training step
        self._train_step = tf.Variable(
            0,
            trainable=False,
            dtype=tf.int32,
            aggregation=tf.VariableAggregation.ONLY_FIRST_REPLICA,
            shape=(),
        )

        # prepare variable container
        self._variables_container = {
            "train_step": self._train_step,
            "policy_variables": self._actor.model.variables,
        }

        # variables signature for variable container table
        variable_container_signature = tf.nest.map_structure(
            lambda variable: tf.TensorSpec(variable.shape, dtype=variable.dtype),
            self._variables_container,
        )

        # Initialize the reverb server
        self.server = reverb.Server(
            tables=[
                reverb.Table(  # Replay buffer
                    name="experience",
                    sampler=reverb.selectors.Uniform(),
                    remover=reverb.selectors.Fifo(),
                    rate_limiter=reverb.rate_limiters.MinSize(learning_starts),
                    max_size=buffer_capacity,
                    max_times_sampled=0,
                    signature={
                        "observation": tf.TensorSpec(
                            [*self._env.observation_space.shape],
                            self._env.observation_space.dtype,
                        ),
                        "action": tf.TensorSpec(
                            [*self._env.action_space.shape],
                            self._env.action_space.dtype,
                        ),
                        "reward": tf.TensorSpec([1], tf.float32),
                        "next_observation": tf.TensorSpec(
                            [*self._env.observation_space.shape],
                            self._env.observation_space.dtype,
                        ),
                        "terminal": tf.TensorSpec([1], tf.float32),
                    },
                ),
                reverb.Table(  # Variable container
                    name="variables",
                    sampler=reverb.selectors.Uniform(),
                    remover=reverb.selectors.Fifo(),
                    rate_limiter=reverb.rate_limiters.MinSize(1),
                    max_size=1,
                    max_times_sampled=0,
                    signature=variable_container_signature,
                ),
            ],
            port=8000,
            checkpointer=checkpointer,
        )

        # Initializes the reverb client
        self.client = reverb.Client("localhost:8000")
        self.tf_client = reverb.TFClient(server_address="localhost:8000")
        self.dataset_iterator = iter(
            reverb.TrajectoryDataset.from_table_signature(
                server_address="localhost:8000",
                table="experience",
                max_in_flight_samples_per_worker=10,
            ).batch(batch_size, drop_remainder=True)
        )

        # init Weights & Biases
        if self._log_wandb:
            wandb.init(project="rl-toolkit")

            # Settings
            wandb.config.max_steps = max_steps
            wandb.config.learning_starts = learning_starts
            wandb.config.buffer_capacity = buffer_capacity
            wandb.config.batch_size = batch_size
            wandb.config.actor_learning_rate = actor_learning_rate
            wandb.config.critic_learning_rate = critic_learning_rate
            wandb.config.alpha_learning_rate = alpha_learning_rate
            wandb.config.tau = tau
            wandb.config.gamma = gamma

        # init actor's params in DB
        self._push_variables()

    def _update_target(self, net, net_targ, tau):
        for source_weight, target_weight in zip(
            net.model.trainable_variables, net_targ.model.trainable_variables
        ):
            target_weight.assign(tau * source_weight + (1.0 - tau) * target_weight)

    def _push_variables(self):
        self.tf_client.insert(
            data=tf.nest.flatten(self._variables_container),
            tables=tf.constant(["variables"]),
            priorities=tf.constant([1.0], dtype=tf.float64),
        )

    # -------------------------------- update critic ------------------------------- #
    def _update_critic(self, batch):
        next_action, next_log_pi = self._actor.predict(batch.data["next_observation"])

        # target Q-values
        next_q_1 = self._critic_targ_1.model(
            [batch.data["next_observation"], next_action]
        )
        next_q_2 = self._critic_targ_2.model(
            [batch.data["next_observation"], next_action]
        )
        next_q = tf.minimum(next_q_1, next_q_2)

        # Bellman Equation
        Q_targets = tf.stop_gradient(
            batch.data["reward"]
            + (1 - batch.data["terminal"])
            * self._gamma
            * (next_q - self._alpha * next_log_pi)
        )

        # update critic '1'
        with tf.GradientTape() as tape:
            q_values = self._critic_1.model(
                [batch.data["observation"], batch.data["action"]]
            )
            q_losses = tf.losses.huber(  # less sensitive to outliers in batch
                y_true=Q_targets, y_pred=q_values
            )
            q1_loss = tf.nn.compute_average_loss(q_losses)

        grads = tape.gradient(q1_loss, self._critic_1.model.trainable_variables)
        self._critic_1.optimizer.apply_gradients(
            zip(grads, self._critic_1.model.trainable_variables)
        )

        # update critic '2'
        with tf.GradientTape() as tape:
            q_values = self._critic_2.model(
                [batch.data["observation"], batch.data["action"]]
            )
            q_losses = tf.losses.huber(  # less sensitive to outliers in batch
                y_true=Q_targets, y_pred=q_values
            )
            q2_loss = tf.nn.compute_average_loss(q_losses)

        grads = tape.gradient(q2_loss, self._critic_2.model.trainable_variables)
        self._critic_2.optimizer.apply_gradients(
            zip(grads, self._critic_2.model.trainable_variables)
        )

        return q1_loss + q2_loss

    # -------------------------------- update actor ------------------------------- #
    def _update_actor(self, batch):
        with tf.GradientTape() as tape:
            # predict action
            y_pred, log_pi = self._actor.predict(batch.data["observation"])

            # predict q value
            q_1 = self._critic_1.model([batch.data["observation"], y_pred])
            q_2 = self._critic_2.model([batch.data["observation"], y_pred])
            q = tf.minimum(q_1, q_2)

            policy_losses = self._alpha * log_pi - q
            policy_loss = tf.nn.compute_average_loss(policy_losses)

        grads = tape.gradient(policy_loss, self._actor.model.trainable_variables)
        self._actor.optimizer.apply_gradients(
            zip(grads, self._actor.model.trainable_variables)
        )

        return policy_loss

    # -------------------------------- update alpha ------------------------------- #
    def _update_alpha(self, batch):
        _, log_pi = self._actor.predict(batch.data["observation"])

        self._alpha.assign(tf.exp(self._log_alpha))
        with tf.GradientTape() as tape:
            alpha_losses = -1.0 * (
                self._log_alpha * tf.stop_gradient(log_pi + self._target_entropy)
            )
            alpha_loss = tf.nn.compute_average_loss(alpha_losses)

        grads = tape.gradient(alpha_loss, [self._log_alpha])
        self._alpha_optimizer.apply_gradients(zip(grads, [self._log_alpha]))

        return alpha_loss

    @tf.function
    def _update(self):
        # Get data from replay buffer
        sample = self.dataset_iterator.get_next()

        # re-new noise matrix every update of 'log_std' params
        self._actor.reset_noise()

        # Alpha param update
        alpha_loss = self._update_alpha(sample)

        # Critic models update
        critic_loss = self._update_critic(sample)

        # Actor model update
        policy_loss = self._update_actor(sample)

        # -------------------- soft update target networks -------------------- #
        self._update_target(self._critic_1, self._critic_targ_1, tau=self._tau)
        self._update_target(self._critic_2, self._critic_targ_2, tau=self._tau)

        # store new actor's params
        if (self._train_step % self._update_interval) == 0:
            self._push_variables()

        return critic_loss, policy_loss, alpha_loss

    def run(self):
        for step in range(self._learning_starts, self._max_steps, 1):
            # update train_step (otlacok modelov)
            self._train_step.assign(step)

            # update models
            critic_loss, policy_loss, alpha_loss = self._update()

            # log metrics
            if (step % self._log_interval) == 0:
                print("=============================================")
                print(f"Step: {step}")
                print(f"Critic loss: {critic_loss}")
                print(f"Policy loss: {policy_loss}")
                print("=============================================")
                print(
                    f"Training ... {tf.floor(self._train_step * 100 / self._max_steps)} %"  # noqa
                )
            if self._log_wandb:
                # log of epoch's mean loss
                wandb.log(
                    {
                        "policy_loss": policy_loss,
                        "critic_loss": critic_loss,
                        "alpha_loss": alpha_loss,
                        "alpha": self._alpha,
                    },
                    step=step,
                )

    def save(self):
        if self._save_path is not None:
            # store models
            self._actor.model.save(os.path.join(self._save_path, "model_A.h5"))
            self._critic_1.model.save(os.path.join(self._save_path, "model_C1.h5"))
            self._critic_2.model.save(os.path.join(self._save_path, "model_C2.h5"))

        # store checkpoint of DB
        self.client.checkpoint()

    def convert(self):
        # Convert the model.
        converter = tf.lite.TFLiteConverter.from_keras_model(self._actor.model)
        tflite_model = converter.convert()

        # Save the model.
        with open("model_A.tflite", "wb") as f:
            f.write(tflite_model)
