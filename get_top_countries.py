# update postgresql config https://www.bigbinary.com/blog/configure-postgresql-to-allow-remote-connection
# restart postgres: /etc/init.d/postgresql restart


# create role https://stackoverflow.com/questions/760210/how-do-you-create-a-read-only-user-in-postgresql
# psql
#CREATE ROLE oleg LOGIN PASSWORD '*';
#GRANT CONNECT ON DATABASE odoo14 TO oleg;
# \c odoo14
#ALTER DEFAULT PRIVILEGES IN SCHEMA public
#   GRANT SELECT ON TABLES TO oleg;



import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab


# Create an engine instance
alchemyEngine = create_engine('postgresql+psycopg2://oleg:test!@37.204.242.84/odoo14', pool_recycle=3600);
 
# Connect to PostgreSQL server
dbConnection = alchemyEngine.connect();

# Read data from PostgreSQL database table and load into a DataFrame instance
df = pd.read_sql("                                                  \
select partner_name,                                                \
       round(100 * cnt / sum(cnt) over (), 1) percent               \
from  (                                                             \
    select partner_name,                                            \
           case when partner_name = 'Other' then 1                  \
                else 0                                              \
           end as ord,                                              \
           sum(cnt) cnt                                             \
    from (                                                          \
        select case when cnt > 17 then partner_name                 \
                    else 'Other'                                    \
               end partner_name,                                    \
               cnt                                                  \
        from (                                                      \
            select coalesce(partner_name, 'Other') partner_name,    \
                   count(1) cnt                                     \
           from crm_lead                                            \
           group by partner_name                                    \
           order by count(1) desc                                   \
        ) t                                                         \
    ) t2                                                            \
    group by partner_name                                           \
) t3                                                                \
order by ord desc, percent;",
dbConnection);


# Close the database connection
dbConnection.close();

TITLE = 'Top IT Outsourcing Countries'
if 1==1:
    TITLE = 'Топ стран по аутсорсингу ИТ'
    df['partner_name'] = df['partner_name'].replace(['United States'], 'США')
    df['partner_name'] = df['partner_name'].replace(['India'], 'Индия')
    df['partner_name'] = df['partner_name'].replace(['United Kingdom'], 'Великобритания')
    df['partner_name'] = df['partner_name'].replace(['Canada'], 'Канада')
    df['partner_name'] = df['partner_name'].replace(['Australia'], 'Австралия')
    df['partner_name'] = df['partner_name'].replace(['Germany'], 'Германия')
    df['partner_name'] = df['partner_name'].replace(['Israel'], 'Израиль')
    df['partner_name'] = df['partner_name'].replace(['Singapore'], 'Сингапур')
    df['partner_name'] = df['partner_name'].replace(['Other'], 'Остальные')


# set style pylab.rcParams.keys()
params = {'legend.fontsize': 'xx-large',
          'figure.figsize' : (9, 9),
          'axes.labelsize' : 'x-large',
          'axes.titlesize' : 'xx-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'ytick.color'    : '#7f7f7f'}
pylab.rcParams.update(params)

# pic size: 1200x627 for LinkedIn https://www.falcon.io/insights-hub/topics/social-media-management/social-media-images-guides/
ax = df.plot.barh(x='partner_name', y='percent', rot=0, color = '#01c952', figsize=(12, 6.27), width=0.7)

# annotate bars
ax.annotate(str(df.percent[0]) + '%', xy=(0            , 0), xytext=(7,  -5), textcoords='offset points', color='white'  , weight = 'light', size  = 'x-large'                                 )

ax.annotate(str(df.percent[1]) + '%', xy=(df.percent[1], 1), xytext=(30, -4), textcoords='offset points', color='#585858', weight = 'light', size  = 'x-large', arrowprops=dict(arrowstyle="-"))
ax.annotate(str(df.percent[2]) + '%', xy=(df.percent[2], 2), xytext=(25, -4), textcoords='offset points', color='#585858', weight = 'light', size  = 'x-large', arrowprops=dict(arrowstyle="-"))
ax.annotate(str(df.percent[3]) + '%', xy=(df.percent[3], 3), xytext=(13, -4), textcoords='offset points', color='#585858', weight = 'light', size  = 'x-large', arrowprops=dict(arrowstyle="-"))

ax.annotate(str(df.percent[4]) + '%', xy=(0,             4), xytext=(7,  -5), textcoords='offset points', color='white'  , weight = 'light', size  = 'x-large'                                 )
ax.annotate(str(df.percent[5]) + '%', xy=(0,             5), xytext=(7,  -5), textcoords='offset points', color='white'  , weight = 'light', size  = 'x-large'                                 )
ax.annotate(str(df.percent[6]) + '%', xy=(0,             6), xytext=(7,  -5), textcoords='offset points', color='white'  , weight = 'light', size  = 'x-large'                                 )
ax.annotate(str(df.percent[7]) + '%', xy=(0,             7), xytext=(7,  -5), textcoords='offset points', color='white'  , weight = 'light', size  = 'x-large'                                 )
ax.annotate(str(df.percent[8]) + '%', xy=(0,             8), xytext=(7,  -5), textcoords='offset points', color='white'  , weight = 'light', size  = 'x-large'                                 )


# add space for lables
plt.subplots_adjust(left=0.2)

plt.title(TITLE)

# Despine
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('#858585')
ax.spines['bottom'].set_visible(False)

# Switch off ticks
ax.tick_params(axis="both", which="both", bottom=False, top=False, labelbottom=False, left=True, right=False, labelleft=True)

# remove the legend if not needed
ax.legend().remove()

y_axis = ax.axes.get_yaxis()
y_axis.set_label_text('')

#plt.show()

plt.savefig('Top IT Outsourcing Countries.png')
plt.close()
