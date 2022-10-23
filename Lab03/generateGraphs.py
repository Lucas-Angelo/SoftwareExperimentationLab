import plotly.express as px
import plotly.graph_objects as go
import pandas

field_names_array = ['reviews', 'code chum', 'analisesTimeInDays', 'bodyHTMLLength',  'comments']

def save_plot(plot, filename):
    plot.show()
#enddef

def calc_a_metrics(df):
    # merged vs closed
    df_merged = df.loc[df['state'] == 'MERGED']
    df_closed = df.loc[df['state'] == 'CLOSED']

    def calc_a_metric(field_name_y_axis):
        def calc_by_state(state, fig):
            df_filtered_state = df.loc[df['state'] == state]
            quartis = df_filtered_state[field_name_y_axis].quantile([0.25,0.5,0.75])
            print(field_name_y_axis, state)
            print(quartis)
            # show graph removing the outliers
            df_no_outliers = df_filtered_state.loc[(df_filtered_state[field_name_y_axis] >= quartis[0.25]) & (df_filtered_state[field_name_y_axis] <= quartis[0.75])]
            fig = fig.add_trace(go.Box(x = df_no_outliers[field_name_y_axis], name=state))
        #enddef

        fig = go.Figure()
        fig.update_layout(title=f"{field_name_y_axis} : MERGED vs CLOSED")

        calc_by_state("MERGED", fig)
        calc_by_state("CLOSED", fig)

        save_plot(fig)
    #enddef

    for i in range(4):
        field_name = field_names_array[i+1]
        calc_a_metric(field_name)
    #endfor
#enddef

def calc_b_metrics (df):
    # removing outliers to graphic

    def calc_b_metric(field_name_y_axis):
        plot = px.scatter(df, x = 'reviews', y=field_name_y_axis)
        save_plot(plot)
    #enddef

    # spearman coefficient calc
    spearman_matrix = df[field_names_array].corr(method="spearman")
    print(spearman_matrix)

    for i in range(4):
        field_name = field_names_array[i+1]
        calc_b_metric(field_name)
    # endfor
#enddef

# init from here: 

df = pandas.read_csv('pullRequests.csv')
df['code chum'] = df.apply(lambda row: row['additions'] + row['deletions'], axis=1)

calc_a_metrics(df)
calc_b_metrics(df)
