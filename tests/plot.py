from app.plot import run_sir_model
from app.plot import generate_sir_plot_image
import os

def test_sir_model_basic():
    S, I, R, t = run_sir_model(1000, 0.3, 0.1, 30)

    assert len(S) == len(I) == len(R) == len(t)
    assert S[0] == 999
    assert I[0] == 1
    assert R[0] == 0

def test_plot_generation(tmp_path):
    abs_path, rel_path, S, I, R = generate_sir_plot_image(
        population=1000,
        beta=0.3,
        gamma=0.1,
        days=30
    )

    assert os.path.exists(abs_path)
    assert abs_path.endswith(".png")