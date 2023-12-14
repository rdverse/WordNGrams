# NLP2

## Setup

To set up the NLP2 project, follow these steps:

1. **Clone the Repository:**

    Use the following command to clone the NLP2 repository:

    ```bash
    git clone https://github.com/rdverse/NLP2.git
    ```

2. **Create a Conda Environment:**

    After cloning, create a Conda environment using the `environment.yml` file:

    ```bash
    conda create -f environment.yml
    ```

3. **Install Environment in Jupyter:**

    If you're using Jupyter Notebook, activate the Conda environment and then install it as a Jupyter kernel:

    ```bash
    # Activate the environment
    conda activate nlppy

    # Install it as a Jupyter kernel
    python -m ipykernel install --user --name nlppy --display-name "nlppy"
    ```

    <!-- Replace `nlppy` with the name of the Conda environment you created.  -->

    To use the environment in Jupyter Notebook, select "nlppy" from the Kernel menu.

4. **How to run:**
    ```
    python3 main.py
    ```


## Google Colab Notebook

Here is the link to the Colab notebook:
- [Link to NLP2 Colab Notebook](#link-to-colab-notebook)