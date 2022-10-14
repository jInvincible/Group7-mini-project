# create chart for Correlation of Participants and Win Rate

df = df_final_stage_count.copy()
sns.lmplot(x='Attend', y='win', data=df)
plt.title('Attend vs Win Rate')
plt.xlabel('Attend')
plt.text(x=11, y=0.7, s='Best fit line', ha='center')
plt.show()
df.corr()