import matplotlib.pyplot as plt
import io
import base64

def run_chart_code(code: str) -> str:
    # Set non-interactive backend
    plt.switch_backend('Agg')
    
    # Prepare execution environment
    local_vars = {}
    exec_env = {
        "plt": plt,
        "np": __import__("numpy"),
        "pd": __import__("pandas")
    }

    try:
        # Remove plt.show() if present in the code
        code = code.replace("plt.show()", "")  

        # Execute the LLM-generated matplotlib code
        exec(code, exec_env, local_vars)

        # Save plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        # Clear plot to avoid overlap in future plots
        plt.clf()

        return image_base64
    except Exception as e:
        return f"Error rendering chart: {str(e)}"
