'''

*** marimekko class module written by james timperley ***

the code is designed to handle a varying number of x categories dynamically to calculate the widths
the x axis can be sorted based on category or value using sort_type
the y categories must be supplied in advance to ensure the sort order is as desired
bar_colours and label_colours are optinal dictionaries to overide the default colours if desired
an exmaple using this module can be found below the marimekko class

'''

from enum import Enum

class SortType(Enum):
    
    CAT_X = 1
    CAT_V = 2
        
class Marimekko:
    
    def __init__(self, df_chart_data, chart_title, cat_x, cat_y, cat_v, y_cats, sort_type, bar_colours, label_colours):
        self.df_chart_data = df_chart_data
        self.chart_title = chart_title
        self.cat_x = cat_x
        self.cat_y = cat_y
        self.cat_v = cat_v
        self.y_cats = y_cats
        self.sort_type = sort_type
        self.bar_colours = bar_colours
        self.label_colours = label_colours
        self.my_data = None
        self.my_widths = None
        self.x_labels = None
        self.my_labels = None
        
    def calculate_variables(self):
        import pandas as pd 
        import numpy as np
        
        # create series of totals
        my_totals = self.df_chart_data.groupby([self.cat_x])[self.cat_v].sum()
        # vvv for development only -- leave commented out            
        # my_totals = df_chart_data.groupby([cat_x])[cat_v].sum()
        # ^^^ for development only -- leave commented out

        # put totals into frame -- sub-totals to be added -- then percantages calculated
        my_calcs = pd.Series(my_totals, name="total")
        my_calcs = my_calcs.to_frame()
        
        # sort frame based on either ascending category or decending value
        if self.sort_type == SortType.CAT_X:
            my_calcs = my_calcs.sort_values(by = [self.cat_x], ascending = [True], na_position = 'first')
        elif self.sort_type == SortType.CAT_V:
            my_calcs = my_calcs.sort_values(by = ['total'], ascending = [False], na_position = 'first')
        
        # add sub-set totals to caclulations frame (based on cat_y)
        # iterate through y_cats doing a group by and sum on the chart data for each one
        # then insert the result into the calculations frame
        # if a sub-total is zero and therefore missing from a sub-category series...
        # ...it will join together correctly because each series has the same index
        for i in range(1, len(self.y_cats)+1, +1):
            temp_series = self.df_chart_data.loc[(self.df_chart_data[self.cat_y] == self.y_cats[i-1])].groupby([self.cat_x])[self.cat_v].sum()
            temp_header = 't' + str(i)
            my_calcs.insert(my_calcs.shape[1],temp_header,temp_series,True)
            my_calcs[temp_header] = my_calcs[temp_header].fillna(0)
        # vvv for development only -- leave commented out            
        # for i in range(1, len(y_cats)+1, +1):
        #     temp_series = df_chart_data.loc[(df_chart_data[cat_y] == y_cats[i-1])].groupby([cat_x])[cat_v].sum()
        #     temp_header = 't' + str(i)
        #     my_calcs.insert(my_calcs.shape[1],temp_header,temp_series,True)
        #     my_calcs[temp_header] = my_calcs[temp_header].fillna(0)
        # ^^^ for development only -- leave commented out
        
        # add %s (sub-set/total)
        # iterate though y_cats and divide each y_cat by the total to get the %s
        # then add each set of %s to the totals frame
        # (this will set the bar heights to get them in proportion)        
        for i in range(1, len(self.y_cats)+1, +1):
            my_calcs['p' +str(i)] = my_calcs['t' + str(i)]/my_calcs['total']
        # vvv for development only -- leave commented out 
        # for i in range(1, len(y_cats)+1, +1):
        #     my_calcs['p' +str(i)] = my_calcs['t' + str(i)]/my_calcs['total']
        # ^^^ for development only -- leave commented out
        
        # create dictionary of %s -- this will be the chart data set
        self.my_data = {self.y_cats[0]: list(my_calcs['p1'])}
        for i in range(2, len(self.y_cats)+1, +1):
            self.my_data.update({self.y_cats[i-1]: list(my_calcs['p' + str(i)])})
        # vvv for development only -- leave commented out
        # my_data = {y_cats[0]: list(my_calcs['p1'])}
        # for i in range(2, len(y_cats)+1, +1):
        #     my_data.update({y_cats[i-1]: list(my_calcs['p' + str(i)])})
        # ^^^ for development only -- leave commented out
        
        # create labels dictionary -- actual totals not %s
        # the iteration that adds traces to the plot will use the data key to extract the label
        self.my_labels = {self.y_cats[0]: list(round(my_calcs['t1']/1000))}
        for i in range(2, len(self.y_cats)+1, +1):
            self.my_labels.update({self.y_cats[i-1]: list(round(my_calcs['t' + str(i)]/1000))})
        # vvv for development only -- leave commented out
        # my_labels = {y_cats[0]: list(round(my_calcs['t1']/1000))}
        # for i in range(2, len(y_cats)+1, +1):
        #     my_labels.update({y_cats[i-1]: list(round(my_calcs['t' + str(i)]/1000))})
        # ^^^ for development only -- leave commented out    
            
        # put totals into a list to calculate width ratios
        #totals_list = list(my_totals)
        totals_list = list(my_calcs['total'])
        
        # calulate widths based on ratio of totals
        w = [i/sum(totals_list) for i in totals_list]
        
        # put widths into an array
        self.my_widths = np.array(w)
        # vvv for development only -- leave commented out
        # my_widths = np.array(w)
        # ^^^ for development only -- leave commented out
        
        # set chart x-axis labels
        self.x_labels = list(my_calcs.index.values)
        # vvv for development only -- leave commented out
        # x_labels = list(my_calcs.index.values)
        # ^^^ for development only -- leave commented out

    def build_chart(self):
    
        import plotly.graph_objects as go
        import plotly.io as pio
        import numpy as np
        
        # set default renderer -- use "pio.renderers" to get full list
        pio.renderers.default = 'svg'
        #pio.renderers.default = 'browser'
        
        # build chart
        fig = go.Figure()
        for key in self.my_data:
            fig.add_trace(go.Bar(
                name=key,
                y=self.my_data[key],
                x=np.cumsum(self.my_widths)-self.my_widths,
                width=self.my_widths,
                offset=0,
                customdata=np.transpose([self.x_labels, self.my_widths*self.my_data[key]]),
                #texttemplate="%{y} x %{width} =<br>%{customdata[1]}",
                texttemplate=self.my_labels[key],
                textposition="inside",
                textangle=0,
                #textfont_color="white",
                #textfont_color=label_colours[key]
                #marker=dict(color=bar_colours[key]),
                # hovertemplate="<br>".join([
                #    "label: %{customdata[0]}",
                #    "width: %{width}",
                #    "height: %{y}",
                #    "area: %{customdata[1]}",
                # ])
            ))
        
        fig.update_xaxes(
            tickvals=np.cumsum(self.my_widths)-self.my_widths/2,
            #ticktext=["%s<br>%d" % (l, w) for l, w in zip(labels, widths)]
            ticktext=[(l) for l  in self.x_labels]
            )
        fig.update_xaxes(range=[0, 1])
        fig.update_yaxes(range=[0, 1], visible=False)
        fig.update_layout(
            title_text=self.chart_title,
            #title={'text': chart_title, 'xanchor': 'left', 'yanchor': 'top'},
            font=dict(size=10),
            barmode="stack",
            uniformtext=dict(mode="hide", minsize=10),
            margin=dict(l=20, r=20, t=50, b=20),
            #paper_bgcolor="LightSteelBlue",
            legend = dict(orientation = "h", xanchor = "center", x = 0.5, y = -0.07),
            ) 
        
        # update bar colours -- if there are any elements in the colours dictionary
        # edit the data dictionary for the figure -- by iterating through the trace indexes
        # base the upper limit on the count of the elements in the colour dictionary
        # create an index for the colours dictionary -- by putting it in a list
        # then use the index to get the key --then use the key get the value
        # (it has to be done like this because the traces in the data dictionary can only be referenced by indexes...
        # ... so a workaround is required to get values from the colours dictionary based on indexes)
        for i in range(0, len(self.bar_colours), +1):
            fig.data[i].update(marker=dict(color=self.bar_colours[list(self.bar_colours)[i]]))
        
        # update font colours -- using the same logic as above
        for i in range(0, len(self.label_colours), +1):
            fig.data[i].update(textfont_color=self.label_colours[list(self.label_colours)[i]])
        
        fig.show()

####################################################################################################################################
### MARIMEKKO EXAMPLE
####################################################################################################################################
# from gen_mods.data_conns import sql_server_connection
# from gen_mods.marimekko import Marimekko, SortType
# import pandas as pd

# my_sql = '''
#         SELECT bse.p02 as fiscal_yr_and_qtr_desc, ccs.cc_segment, chn.derived_channel, prd.product_description, bse.market_area, mvt.movement_category, SUM(bse.net_movement) as net_movement
#         FROM tbl_fact_base_evol AS bse
#         LEFT OUTER JOIN tbl_dim_movement_category AS mvt ON bse.mvt_id = mvt.mvt_id
#         LEFT OUTER JOIN tbl_dim_cc_segment AS ccs ON bse.ccs_id = ccs.ccs_id
#         LEFT OUTER JOIN tbl_dim_derived_channel AS chn ON bse.chn_id = chn.chn_id
#         LEFT OUTER JOIN vw_dim_product AS prd ON bse.product_name = prd.product_name
#         WHERE 1=1
#             --AND bse.market_area in('BEN','EE','FRA','GER','IBE','ITA','ME','NORD','RCIS','SSAI','SWI','UK')
#             AND bse.market_area in('BEN','FRA','GER','EE','IBE','ITA','ME','NORD','RCIS', 'UK')
#             --AND cc_segment <> '<UNKNOWN>'
#             AND ccs.cc_segment = 'TEAM'           
#             --AND chn.derived_channel = 'RESELLER'
#             AND mvt.movement_category in('06. Other Increases', '05. Increased Units', '04. Added Products', '03. Added Segments', '02. Returned Customers', '01. New Customers')
#             AND bse.p02 = '2021-Q3'
#         GROUP BY p02, ccs.cc_segment, chn.derived_channel, prd.product_description, bse.market_area, mvt.movement_category
#         ORDER BY p02, ccs.cc_segment, chn.derived_channel, prd.product_description, bse.market_area, mvt.movement_category
#         '''
    
# ds = sql_server_connection('gtm')
# base_data = pd.read_sql(my_sql, ds.connection)

# my_marimekko = Marimekko(
#                         df_chart_data = base_data
#                         , chart_title = 'New Business (Numbers in 000s)'
#                         , cat_x = 'market_area'
#                         , cat_y = 'movement_category'
#                         , cat_v = 'net_movement'
#                         , y_cats = ['06. Other Increases', '05. Increased Units', '04. Added Products', '03. Added Segments', '02. Returned Customers', '01. New Customers']
#                         , sort_type = SortType.CAT_X
#                         , bar_colours = {
#                                         '06. Other Increases': 'rgb(166, 199, 233)'
#                                         , '05. Increased Units': 'rgb(241,206,99)'
#                                         , '04. Added Products': 'rgb(121,111,110)'
#                                         , '03. Added Segments': 'rgb(70,120,173)'
#                                         , '02. Returned Customers': 'rgb(241,142,43)'
#                                         , '01. New Customers': 'rgb(89,161,80)'
#                                         }
#                         , label_colours = {
#                                         '06. Other Increases': 'black'
#                                         , '05. Increased Units': 'black'
#                                         , '04. Added Products': 'white'
#                                         , '03. Added Segments': 'white'
#                                         , '02. Returned Customers': 'black'
#                                         , '01. New Customers': 'white'
#                                         }
#                         )

# my_marimekko.calculate_variables()
# my_marimekko.build_chart()
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

####################################################################################################################################
### MATPLOTLIB VERSION
####################################################################################################################################
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # calculate bar totals and sub-set sub-totals
# t = df_chart_data.groupby(['market_area'])['net_movement'].sum()
# t1 = df_chart_data.loc[(df_chart_data['movement_category'] == '01. New Customers')].groupby(['market_area'])['net_movement'].sum()
# t2 = df_chart_data.loc[(df_chart_data['movement_category'] == '03. Added Segments')].groupby(['market_area'])['net_movement'].sum()
# t3 = df_chart_data.loc[(df_chart_data['movement_category'] == '05. Increased Units')].groupby(['market_area'])['net_movement'].sum()

# # calculate bar % splits based on the above
# y1 = list(t1/t)
# y2 = list(t2/t)
# y3 = list(t3/t)

# fig, ax = plt.subplots(1)
# # put totals into a list to calculate width ratios
# x2 = list(t)
# # calulate widths based on ratio of totals
# w = [i/sum(x2) for i in x2]
# # set x-axis labels as distinct list of market areas
# x_label = list(df_chart_data['market_area'].unique())

# # calculate x coordinates based on the width of the previous bars
# adjusted_x2, temp = [0], 0
# for i in w[:-1]:
#     temp += i
#     adjusted_x2.append(temp)
  
# # Marimekko chart
# # add y1
# plt.bar(adjusted_x2, y1, width=w, align='edge', edgecolor='black')
# # add b on top of y1
# plt.bar(adjusted_x2, y2, bottom=y1, width=w, align='edge', edgecolor='black')
# # add con top of y1 + y3
# plt.bar(adjusted_x2, y3, bottom=np.add(y1,y2), width=w, align='edge', edgecolor='black')

# # x and y ticks (%)
# #ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
# #ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])
# #ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
# #ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])

# #ax.spines['top'].set_color('red')
# #ax.spines['right'].set_color('red')
# #ax.spines['bottom'].set_color('red')
# #ax.spines['left'].set_color('red')

# plt.ylim(0,1)
# plt.xlim(0,1)

# # twin y-axis to draw x-ticks at the top
# axy = ax.twiny()
# axy.set_xticks([(w[i]/2)+ v for i, v in enumerate(adjusted_x2)])
# axy.set_xticklabels(x_label, fontsize=10)

# plt.show()
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

####################################################################################################################################
### PLOTLY EXPRESS SUNBURST
####################################################################################################################################
# df_sunburst = (df_base_data.loc[
#                 (df_base_data['cc_segment'].isin(['TEAM','ACROBAT DC','SIGN','STOCK']))
#                 & (df_base_data['movement_category'].isin(['01. New Customers']))
#                 & (df_base_data['fiscal_yr_and_qtr_desc'].isin(['2021-Q2']))
#                 ])

# import plotly.express as px
# fig = px.sunburst(df_sunburst, path=['product_description', 'market_area'], values='net_movement')
# fig.show()
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################