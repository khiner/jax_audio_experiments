import jax.numpy as jnp
from jax import jit

from jaxdsp.processors.base import Config, default_param_values
from jaxdsp.param import Param

NAME = "Sine Wave"
PARAMS = [
    Param("frequency_hz", 400.0, 30.0, 10_000.0, log_scale=True),
]
PRESETS = {}


def config():
    return Config(
        {"phase_radians": 0.0, "sample_rate": 44100},
        default_param_values(PARAMS),
        {"frequency_hz": 443.0},
    )


@jit
def tick(carry, x):
    raise "single-sample tick method not implemented for sine_wave"


@jit
def tick_buffer(carry, X):
    params = carry["params"]
    state = carry["state"]
    # Add an extra sample to determine phase for start of next buffer.
    t = jnp.arange(X.size + 1) / state["sample_rate"]
    x = params["frequency_hz"] * 2 * jnp.pi * t + state["phase_radians"]
    state["phase_radians"] = x[-1] % (2 * jnp.pi)
    return carry, jnp.sin(x[:-1])
