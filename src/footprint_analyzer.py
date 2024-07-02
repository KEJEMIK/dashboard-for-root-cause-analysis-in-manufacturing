import matplotlib.pyplot as plt
import pm4py
import numpy as np
import graphviz_helper

class FootprintKpi:
    """
    Represents aggregated Key Performance Indicator (KPI) values for a given Footprint.

    Attributes:
        oee (float): Overall Equipment Effectiveness (OEE) value.
        lead_time (float): Lead time value (seconds).
        malfunction_duration (float): Malfunction duration value (seconds).
        rejection_count (float): Number of rejected materials.
        count (int): Count of footprints.
    """
    def __init__(self, oee, lead_time, malfunction_duration, rejection_count, count):
        self.oee = oee
        self.lead_time = lead_time
        self.malfunction_duration = malfunction_duration
        self.rejection_count = rejection_count
        self.count = count

class EdgeMarking:
    """
    Represents a directed edge in a Directly Follows Graph (DFG) with assigned color.

    Attributes:
        src (str): Source node of the edge.
        dest (str): Destination node of the edge.
        color (str): Color of the edge.
    """
    def __init__(self, src, dest, color):
        self.src = src
        self.dest = dest
        self.color = color

red_pallete = ['#F15A59', '#ED2B2A', '#D21312', '#850000']
green_pallete = ['#D0E7D2', '#B0D9B1', '#79AC78', '#618264']

def calculate_outlier_footprints(footprints, values, mean, sd, kpi):
    """
    Calculate outlier footprints based on the given KPI values and assign colors to them.

    Parameters:
        footprints (list): List of footprints.
        values (list): List of KPI values.
        mean (float): Mean value of the KPI.
        sd (float): Standard deviation of the KPI.
        kpi (str): Key Performance Indicator.

    Returns:
        tuple: A tuple containing lists of outlier footprints and their corresponding colors.
    """
    
    outliers = []
    outlier_colors = []
    for i in range(len(values)):
        val = values[i]
        fp = footprints[i]
        if kpi == 'OEE':
            fp_color = determine_color(val, mean + (sd /2), mean - sd, sd, True)
        else:
            fp_color = determine_color(val, mean + sd, mean - (sd /2), sd, False)
        if fp_color != 'blue':
            outliers.append(fp)
            outlier_colors.append(fp_color)

    return outliers, outlier_colors

def determine_color(val, upper_bound, lower_bound, sd, reverse):
    """
    Determine the color for the given KPI value based on upper and lower bounds.

    Parameters:
        val (float): KPI value to determine the color for.
        upper_bound (float): Upper bound for the KPI.
        lower_bound (float): Lower bound for the KPI.
        sd (float): Standard deviation of the KPI.
        reverse (bool): Indicates if the bounds are reversed.

    Returns:
        str: Color code for the value.
    """
    
    if reverse == True:
        if val > upper_bound:
            if val <= upper_bound + sd:
                return green_pallete[0]
            elif val <= upper_bound + 2 * sd:
                return green_pallete[1]
            elif val <= upper_bound + 3 * sd:
                return green_pallete[2]
            return green_pallete[3]
        elif val < lower_bound:
            if val >= lower_bound - sd:
                return red_pallete[0]
            elif val >= lower_bound - 2 * sd:
                return red_pallete[1]
            elif val >= lower_bound - 3 * sd:
                return red_pallete[2]
            return red_pallete[3]
        else:
            return 'blue'

    if val > upper_bound:
        if val <= upper_bound + sd:
            return red_pallete[0]
        elif val <= upper_bound + 2 * sd:
            return red_pallete[1]
        elif val <= upper_bound + 3 * sd:
            return red_pallete[2]
        return red_pallete[3]
    elif val < lower_bound:
        if val >= lower_bound - sd:
            return green_pallete[0]
        elif val >= lower_bound - 2 * sd:
            return green_pallete[1]
        elif val >= lower_bound - 3 * sd:
            return green_pallete[2]
        return green_pallete[3]
    else:
        return 'blue'

def draw_footprint_kpi_scatter(labels, values, mean, sd, title, xlabel, ylabel):
    """
    Draw scatter plot for Footprint KPIs.

    Parameters:
        labels (list): List of labels.
        values (list): List of KPI values.
        mean (float): Mean value of the KPI.
        sd (float): Standard deviation of the KPI.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
    """
    
    num_data_points = len(labels)

    # Set the minimum size
    min_figsize = (16, 12)

    if num_data_points > 100:
        size_increment = (16, 12)
        num_100s = num_data_points // 100
        figsize = (min_figsize[0] + size_increment[0] * num_100s, min_figsize[1] + size_increment[1] * num_100s)
    else:
        figsize = min_figsize

    # Create a scatter plot
    plt.figure(figsize=figsize)
    if ylabel == 'OEE':
        colors = [determine_color(val, mean + (sd / 2), mean - sd, sd, True) for val in values]
    else:
        colors = [determine_color(val, mean + sd, mean - (sd / 2), sd, False) for val in values]
    plt.scatter(labels, values, marker='o', c=colors)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability

    plt.axhline(y=mean, color='red', linestyle='--', label=f'Mean')

    if ylabel == 'OEE':
        plt.axhline(y=mean + (sd / 2), color='blue', linestyle='--', label=f'Confidence interval')
        plt.axhline(y=mean - sd if mean - sd > 0 else 0, color='blue', linestyle='--')
    else:
        plt.axhline(y=mean + sd, color='blue', linestyle='--', label=f'Confidence interval')
        plt.axhline(y=mean - (sd / 2) if mean - (sd / 2) > 0 else 0, color='blue', linestyle='--')
    plt.legend()

    plt.grid()
    plt.tight_layout()
    plt.show()

def extract_footprints(data, time, case_id, activity):
    """
    Extract footprints from event log data.

    Parameters:
        data (pd.DataFrame): Input DataFrame.
        time (str): Name of the time column.
        case_id (str): Name of the case ID column.
        activity (str): Name of the activity column.

    Returns:
        dict: Extracted footprints.
    """

    temp = data.loc[data['End Date Actual'].notna()]
    temp = temp.rename(columns={time: 'time:timestamp', case_id: 'case:concept:name', activity: 'concept:name'})
    extracted_footprints = pm4py.discover_footprints(temp)['dfg']
    
    return extracted_footprints

def extract_kpi_information(data):
    """
    Extracts Key Performance Indicator (KPI) information for a given material number.

    Parameters:
        data (pd.DataFrame): Production data for a given material number.

    Returns:
        pd.DataFrame: DataFrame containing KPI information for a material number.
    """

    # Extract KPI information for the material number
    kpi_data_mnummer = data.agg({
        'OEE': 'mean',
        'Lead Time': 'mean',
        'Malfunction Duration': 'mean',
        'Rejected Materials': ['mean'],
    }).reset_index()

    # Rename the columns to be more descriptive
    kpi_data_mnummer.columns = ['Contract', 'OEE',
                                'Lead Time', 'Malfunction Duration', 'Rejected Materials']

    kpi_data_mnummer['Malfunction Duration'] = kpi_data_mnummer[(
        'Malfunction Duration')].dt.total_seconds()
    kpi_data_mnummer['Lead Time'] = kpi_data_mnummer[(
        'Lead Time')].dt.total_seconds()

    return kpi_data_mnummer

def analyze_footprints_by_kpi(data, contracts, kpi_data_mnummer):
    """
    Performs footprint analysis by KPIs. Firstly, the function extracts footprints from the data, then it calculates aggregated KPI values for each of the extracted footprints.

    Parameters:
        data (pd.DataFrame): Production data.
        contracts (list): List of contract values.
        kpi_data_mnummer (pd.DataFrame): DataFrame containing KPI data.

    Returns:
        tuple: A tuple containing aggregated KPI values for footprints, dictionary describing in which contracts a footprint appears, and differences of the footprint KPI values to target.
    """
    
    time = 'End Date Actual'
    activity = 'Operation RelNr'
    case_id = 'Contract'

    extracted_footprints = extract_footprints(data, time, case_id, activity)

    footprint_kpis = {}
    footprint_contracts = {}

    for contract in contracts:

        # Filter data
        pg_df_filtered = data.loc[data["Contract"] == contract]

        # Extract KPI data
        kpi_data = pg_df_filtered.groupby(['Contract']).agg({
            'OEE': 'mean',
            'Lead Time': 'mean',
            'Malfunction Duration': 'mean',
            'Rejected Materials': ['mean', 'count'],
        }).reset_index()

        # Rename the columns to be more descriptive
        kpi_data.columns = ['Contract', 'OEE', 'Lead Time', 'Malfunction Duration', 'Rejected Materials', 'Counter']

        kpi_data['Malfunction Duration'] = kpi_data[('Malfunction Duration')].dt.total_seconds()
        kpi_data['Lead Time'] = kpi_data[('Lead Time')].dt.total_seconds()

        # Extract footprints
        pg_df_filtered = pg_df_filtered.loc[pg_df_filtered['End Date Actual'].notna()]
        pg_df_filtered = pg_df_filtered.rename(columns={time: 'time:timestamp', case_id: 'case:concept:name', activity: 'concept:name'})

        footprints = pm4py.discover_footprints(pg_df_filtered)

        # Check if any of the discovered footprints are in the 
        # extracted_footprints table, if they are, 
        # add the KPI values to the found footprint
        for fp in extracted_footprints:
            if fp in footprints['dfg'].keys():
                if fp not in footprint_kpis.keys():
                    footprint_kpis[fp] = FootprintKpi(kpi_data['OEE'].iloc[0], kpi_data['Lead Time'].iloc[0], kpi_data['Malfunction Duration'].iloc[0], kpi_data['Rejected Materials'].iloc[0], 1)
                else:
                    footprint_kpis[fp].oee = footprint_kpis[fp].oee + kpi_data['OEE'].iloc[0]
                    footprint_kpis[fp].lead_time = footprint_kpis[fp].lead_time + kpi_data['Lead Time'].iloc[0]
                    footprint_kpis[fp].malfunction_duration = footprint_kpis[fp].malfunction_duration + kpi_data['Malfunction Duration'].iloc[0]
                    footprint_kpis[fp].rejection_count = footprint_kpis[fp].rejection_count + kpi_data['Rejected Materials'].iloc[0]
                    footprint_kpis[fp].count = footprint_kpis[fp].count + 1
                
                if fp not in footprint_contracts.keys():
                    footprint_contracts[fp] = [contract]
                else:
                    footprint_contracts[fp].append(contract)

    # Analyze each footprint's KPIs 
    # append the means to the tables for plotting
    footprints_for_calc = []
    footprints_to_plot = []
    oees = []
    oees_diff_to_soll = []
    lead_times = []
    lead_times_diff_to_soll = []
    malfunction_durations = []
    malfunction_durations_diff_to_soll = []
    rejection_counts = []
    rejection_counts_diff_to_soll = []

    for fp in extracted_footprints:
        # We only consider footprints present in footprint_kpis map
        if (fp not in footprint_kpis.keys()):
            continue

        # Calculate the KPI means
        oee = footprint_kpis[fp].oee / footprint_kpis[fp].count
        lead_time = footprint_kpis[fp].lead_time / footprint_kpis[fp].count
        malfunction_duration = footprint_kpis[fp].malfunction_duration / footprint_kpis[fp].count
        rejection_count = footprint_kpis[fp].rejection_count / footprint_kpis[fp].count

        oee_diff_to_soll = oee - kpi_data_mnummer['OEE'].iloc[0]
        lead_time_diff_to_soll = lead_time - kpi_data_mnummer['Lead Time'].iloc[0]
        malfunction_duration_diff_to_soll = malfunction_duration - kpi_data_mnummer['Malfunction Duration'].iloc[0]
        rejection_count_diff_to_soll = rejection_count - kpi_data_mnummer['Rejected Materials'].iloc[0]

        # Append to the tables for plotting
        footprints_for_calc.append(fp)
        footprints_to_plot.append(fp[0] + ' -> ' + fp[1])
        oees.append(oee)
        oees_diff_to_soll.append(oee_diff_to_soll)
        lead_times.append(lead_time)
        lead_times_diff_to_soll.append(lead_time_diff_to_soll)
        malfunction_durations.append(malfunction_duration)
        malfunction_durations_diff_to_soll.append(malfunction_duration_diff_to_soll)
        rejection_counts.append(rejection_count)
        rejection_counts_diff_to_soll.append(rejection_count_diff_to_soll)

    kpi_values = {'fp': footprints_for_calc, 'label': footprints_to_plot, 'OEE': oees, 'Lead Time': lead_times, 'Malfunction Duration': malfunction_durations, 'Rejected Materials': rejection_counts}
    diff_to_soll = {'Footprint': footprints_to_plot, 'OEE': oees_diff_to_soll, 'Lead Time': lead_times_diff_to_soll, 'Malfunction Duration': malfunction_durations_diff_to_soll, 'Rejected Materials': rejection_counts_diff_to_soll}

    return kpi_values, footprint_contracts, diff_to_soll   

def calcualte_kpi_means(data):
    """
    Calculates means of Key Performance Indicators (KPIs).

    Parameters:
        data (pd.DataFrame): Production data for which the KPI means are to be calculated.

    Returns:
        dict: Dictionary containing KPI means.
    """

    oee_total_mean = data['OEE'].mean()
    lead_times_total_mean = data['Lead Time'].mean().total_seconds()
    malfunction_durations_total_mean = data['Malfunction Duration'].mean().total_seconds()
    rejection_counts_total_mean = data['Rejected Materials'].mean()

    kpi_means = {'OEE': oee_total_mean, 'Lead Time': lead_times_total_mean, 'Malfunction Duration': malfunction_durations_total_mean, 'Rejected Materials': rejection_counts_total_mean}
    return kpi_means

def calculate_sds(kpi_data):
    """
    Calculates standard deviations of Key Performance Indicators (KPIs).

    Parameters:
        kpi_data (pd.DataFrame): DataFrame containing KPI data.

    Returns:
        dict: Dictionary containing KPI standard deviations.
    """

    oee_sd = np.std(kpi_data['OEE'])
    lead_times_sd = np.std(kpi_data['Lead Time'])
    malfunction_durations_sd = np.std(kpi_data['Malfunction Duration'])
    rejection_counts_sd = np.std(kpi_data['Rejected Materials'])

    kpi_sds = {'OEE': oee_sd, 'Lead Time': lead_times_sd, 'Malfunction Duration': malfunction_durations_sd, 'Rejected Materials': rejection_counts_sd}
    return kpi_sds

def filter_data_by_contract(data_to_filter, contracts):
    """
    Filters data by contract values.

    Parameters:
        data_to_filter (pd.DataFrame): Production data to be filtered.
        contracts (list): List of contract values to filter by.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """

    time = 'End Date Actual'
    activity = 'Operation RelNr'
    case_id = 'Contract'

    curr = data_to_filter
    curr = curr.loc[curr["Contract"].isin(contracts)]
    curr = curr.loc[curr['End Date Actual'].notna()]
    curr = curr.rename(columns={time: 'time:timestamp', case_id: 'case:concept:name', activity: 'concept:name'})
    return curr

def extract_dfg_for_contracts(data, contracts):
    """
    Extracts Directly-Follows Graph (DFG) for Auftrag values.

    Parameters:
        data (pd.DataFrame): Production data.
        auftrags (list): List of Auftrag values.

    Returns:
        pm4py.visualization.dfg.Visualization: Extracted DFG.
    """

    curr = filter_data_by_contract(data, contracts)

    return pm4py.discover_dfg(curr)

def extract_edge_markings(fps, fps_colors):
    """
    Extracts edge markings for footprints.

    Parameters:
        fps (list): List of footprints.
        fps_colors (list): List of corresponding colors.

    Returns:
        list: List of EdgeMarking objects.
    """

    edge_markings = []

    for i in range(len(fps)):
        fp = fps[i]
        marking_color = fps_colors[i]
        edge_markings.append(EdgeMarking(fp[0], fp[1], marking_color))

    return edge_markings

def draw_dfg_for_footprint(data, contracts, em):
    """
    Draws Directly-Follows Graph (DFG) for footprints.

    Parameters:
        data (pd.DataFrame): Production data.
        contracts (list): List of contracts for which DFG should be drawn.
        em (list): List of EdgeMarking objects to be applied to DFG drawing.
    """

    dfg = extract_dfg_for_contracts(data, contracts)
    graphviz_helper.view_graphviz_dfg(dfg, em)