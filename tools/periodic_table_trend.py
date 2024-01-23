import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

class PeriodicTablePlotter:
    def __init__(self):
        self.initialized = False

    def initialize(self):
        # periodic_table_dict: get element name, row index, and group index
        with open('periodic_table_dict.json') as json_file:
            periodic_table_dict_raw = json.load(json_file)

        self.periodic_table_dict = dict()
        for z_string in periodic_table_dict_raw:
            self.periodic_table_dict[int(z_string)] = periodic_table_dict_raw[z_string]


        # periodic_table_df
        self.periodic_table_df = self._get_periodic_table_df()

        # name_z_dict
        self.name_z_dict = self._get_name_z_dict()

        self.initialized = True

    def _get_periodic_table_df(self) -> pd.DataFrame:
        """
        RETURNS:
            periodic_table_df(pd.DataFrame)
        """

        periodic_table_df = pd.DataFrame(columns=range(18), index=range(9))
        for z in range(1, 119):
            tem_name = self.periodic_table_dict[z][0]
            tem_row = self.periodic_table_dict[z][1]
            tem_group = self.periodic_table_dict[z][2]

            periodic_table_df.loc[tem_row-1, tem_group-1] = tem_name
        return(periodic_table_df)

    def _get_name_z_dict(self) -> pd.DataFrame:
        """
        RETURNS:
            name_z_dict(dict of str: int): key: element name, value: z number
        """

        name_z_dict = dict()
        for z in range(1, 119):
            tem_name = self.periodic_table_dict[z][0]
            name_z_dict[tem_name] = z
        return(name_z_dict)


    def get_plot(self, value_dic):
        """
        PARAMS:
            value_dic(dict of str: int/float): keys: element name(str). values: quantity of the given element
        """
        if not self.initialized:
            raise RuntimeError('Please initialize PeriodicTablePlotter by calling PeriodicTablePlotter.initialize()') from error
        
        periodic_table_count_np = np.zeros(shape=(9, 18))
        for element_name in value_dic:
            tem_z = self.name_z_dict[element_name]
            tem_row = self.periodic_table_dict[tem_z][1]
            tem_group = self.periodic_table_dict[tem_z][2]
            periodic_table_count_np[tem_row-1][tem_group-1] = value_dic[element_name]
            
        # plot
        fig, ax = plt.subplots(figsize=(8, 10))

        im = ax.imshow(periodic_table_count_np, cmap='hot')
        # annotation
        for i in range(9):
            for j in range(18):
                if not pd.isna(self.periodic_table_df.loc[i, j]):
                    ax.annotate(str(self.periodic_table_df.loc[i, j]), xy=(j, i),
                                 ha='center', va='center', color='grey')
        plt.axis('off')
        cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
        plt.colorbar(im, cax=cax)
        self.fig = fig

    def save_plot(self, filename: str, **kwargs):
        """
        Save matplotlib plot to a file.

        Args:
            filename (str): Filename to write to. Must include extension to specify image format.
        """
        if not self.initialized:
            raise RuntimeError('Please initialize PeriodicTablePlotter by calling PeriodicTablePlotter.initialize()') from error
        if not self.fig:
            raise RuntimeError('Please plot by calling PeriodicTablePlotter.get_plot()') from error
        self.fig.savefig(filename, bbox_inches='tight')
