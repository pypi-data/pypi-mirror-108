import argparse
import gym
import pybullet_envs  # noqa

# policy
from rl_toolkit.policy import Learner, Agent, Tester

if __name__ == "__main__":

    my_parser = argparse.ArgumentParser(
        prog="python3 -m rl_toolkit",
        description="The RL-Toolkit: A toolkit for developing and comparing your reinforcement learning agents in various games (OpenAI Gym or Pybullet).",  # noqa
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    my_parser.add_argument(
        "-env",
        "--environment",
        type=str,
        help="Only OpenAI Gym/PyBullet environments are available!",
        required=True,
    )
    my_parser.add_argument(
        "--mode",
        choices=["agent", "learner", "tester"],
        help="Choose operating mode.",
        required=True,
    )
    my_parser.add_argument(
        "-t",
        "--max_steps",
        type=int,
        help="Number of agent's steps",
        default=int(1e6),
    )
    my_parser.add_argument(
        "--gamma",
        type=float,
        help="Discount rate (gamma) for future rewards",
        default=0.99,
    )
    my_parser.add_argument(
        "--tau",
        type=float,
        help="Parameter for soft target network updates",
        default=0.01,
    )
    my_parser.add_argument(
        "-lr",
        "--learning_rate",
        type=float,
        help="Learning rate for policy & critic networks",
        default=7.3e-4,
    )
    my_parser.add_argument(
        "--batch_size", type=int, help="Size of the mini-batch", default=256
    )
    my_parser.add_argument(
        "--buffer_capacity",
        type=int,
        help="Maximum capacity of replay memory",
        default=int(1e6),
    )
    my_parser.add_argument(
        "--learning_starts",
        type=int,
        help="Number of steps before using policy network",
        default=10000,
    )
    my_parser.add_argument(
        "--env_steps", type=int, help="Num. of environment steps", default=64
    )
    my_parser.add_argument(
        "--log_interval", type=int, help="Log into console interval", default=64
    )
    my_parser.add_argument(
        "--render", action="store_true", help="Render the environment"
    )
    my_parser.add_argument("--wandb", action="store_true", help="Log into WanDB cloud")
    my_parser.add_argument("-s", "--save", type=str, help="Path for saving model files")
    my_parser.add_argument("--model_a", type=str, help="Actor's model file")
    my_parser.add_argument("--model_c1", type=str, help="Critic 1's model file")
    my_parser.add_argument("--model_c2", type=str, help="Critic 2's model file")
    my_parser.add_argument("--db_path", type=str, help="DB's checkpoints path")
    my_parser.add_argument(
        "--db_server", type=str, help="DB server name", default="localhost"
    )

    # nacitaj zadane argumenty programu
    args = my_parser.parse_args()

    # Herne prostredie
    env = gym.make(args.environment)

    print("Action space:")
    print(env.action_space)
    print(env.action_space.low, env.action_space.high)
    print()
    print("Observation space:")
    print(env.observation_space)
    print(env.observation_space.low, env.observation_space.high)
    print()

    # Agent mode
    if args.mode == "agent":
        agent = Agent(
            db_server=args.db_server,
            env=env,
            env_steps=args.env_steps,
            learning_starts=args.learning_starts,
            log_wandb=args.wandb,
        )

        try:
            # run actor process
            agent.run()
        except KeyboardInterrupt:
            print("Terminated by user 👋👋👋")
        finally:
            # zatvor herne prostredie
            env.close()

    # Learner mode
    if args.mode == "learner":
        agent = Learner(
            env=env,
            max_steps=args.max_steps,
            learning_starts=args.learning_starts,
            buffer_capacity=args.buffer_capacity,
            batch_size=args.batch_size,
            actor_learning_rate=args.learning_rate,
            critic_learning_rate=args.learning_rate,
            alpha_learning_rate=args.learning_rate,
            tau=args.tau,
            gamma=args.gamma,
            model_a_path=args.model_a,
            model_c1_path=args.model_c1,
            model_c2_path=args.model_c2,
            save_path=args.save,
            db_path=args.db_path,
            log_wandb=args.wandb,
            log_interval=args.log_interval,
        )

        try:
            # run training process
            agent.run()
        except KeyboardInterrupt:
            print("Terminated by user 👋👋👋")
        finally:
            # zatvor herne prostredie
            env.close()

            # save models and snapshot of the database
            agent.save()

    # Test mode
    elif args.mode == "tester":
        agent = Tester(
            env=env,
            max_steps=args.max_steps,
            model_a_path=args.model_a,
            log_wandb=args.wandb,
        )

        try:
            # run actor process
            agent.run(render=args.render)
        except KeyboardInterrupt:
            print("Terminated by user 👋👋👋")
        finally:
            # zatvor herne prostredie
            env.close()
