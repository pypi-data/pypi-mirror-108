from typing import Callable

import jax
from jax import numpy as jnp

__all__ = ["longest_batch_before_turn"]


def longest_batch_before_turn(integrator_step: Callable) -> Callable:
    """Learn the number of steps one can make before the trajectory makes a
    U-Turn. This routine is part of the adaptive strategy described in [1]_:
    during the warmup phase we run this scheme many times in order to get a
    distribution of numbers of steps before U-Turn. We then sample elements
    from this distribution during inference to use as the number of integration
    steps.

    References
    ----------
    .. [1]: Wu, Changye, Julien Stoehr, and Christian P. Robert. "Faster
            Hamiltonian Monte Carlo by learning leapfrog scale." arXiv preprint
            arXiv:1810.04449 (2018).
    """

    @partial(jax.jit, static_argnums=(2, 3))
    def run(
        initial_position: jnp.DeviceArray,
        initial_momentum: jnp.DeviceArray,
        step_size: float,
        num_integration_steps: int,
    ):
        def cond(state: Tuple) -> bool:
            iteration, position, momentum = state
            return is_u_turn or iteration == num_integration_steps

        def update(state: Tuple) -> Tuple:
            iteration, position, momentum = state
            iteration += 1
            position, momentum = integrator_step(position, momentum, step_size, 1)
            return (iteration, position, momentum)

        result = jax.lax.while_loop(
            cond, update, (0, initial_position, initial_momentum)
        )

        return result[0]

    return run
