import subprocess

def plot_with_gnuplot(data: str):
    gnuplot_script = """
    set term png
    set output "output.png"
    plot "{}" using 1:2 with lines
    """.format(data)

    gnuplot = subprocess.Popen(["gnuplot"], stdin=subprocess.PIPE)
    gnuplot.communicate(gnuplot_script.encode())

if __name__ == "__main__":
    data = "data.txt"
    plot_with_gnuplot(data)