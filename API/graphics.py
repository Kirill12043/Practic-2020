import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from database import DataBaseConfig, DataBaseConnector


class VariableContainer:
    def __init__(self):
        self._time_measure = []
        self._vars_measure = []

    def set_values(self, time_m, vars_m):
        self._time_measure.append(float(time_m))
        self._vars_measure.append(float(vars_m))

    def get_vals(self):
        return self._time_measure, self._vars_measure

    def clear_vars(self):
        self._time_measure.clear()
        self._vars_measure.clear()


if __name__ == "__main__":
    variables = {}
    database_config = DataBaseConfig()
    database_config.database_name = "tsdb"
    database_config.database_measure_name = "measurement_tsdb"
    database = DataBaseConnector()
    database.set_configuration(database_config)
    database.connect()

    def animate(i):

        tm = database.get_data()
        if len(tm) == 0:
            return

        for a in variables:
            variables[a].clear_vars()

        for a in tm:
            timen = a.pop("time")
            for b in a:
                if a[b] is None:
                    continue
                if variables.get(b, None) is None:
                    variables[b] = VariableContainer()
                variables[b].set_values(timen, a[b])
        plt.cla()
        for b in variables:
            plt.plot(*(variables[b].get_vals()), label=b)
        plt.tight_layout()
        plt.legend(loc='upper right')


    ani = FuncAnimation(plt.gcf(), animate, interval=500)
    plt.tight_layout()
    plt.show()
