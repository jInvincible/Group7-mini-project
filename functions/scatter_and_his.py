df = df_final_stage_count.copy()
fig, axs = plt.subplots(figsize=(9,6), nrows=2, ncols=2, sharex="col", sharey="row", 
                         gridspec_kw=dict(height_ratios=[1, 3],
                                          width_ratios=[3, 1]))
plt.title('Semi-finals and Finals Participants vs Win Rate', x=-1.2, y = -0.3)

axs[0, 1].set_visible(False)
axs[0, 0].set_box_aspect(1/3)
axs[1, 0].set_box_aspect(1)
axs[1, 1].set_box_aspect(2.5/1)

x = df['Attend']
y = df['win']
axs[1, 0].scatter(x, y)
axs[1, 0].plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
axs[1, 0].text(x=7.5, y= 0.6, s='Best fit line', rotation=30)
axs[1, 0].set_xlabel('Attend')
axs[1, 0].set_ylabel('Win Rate')
axs[0, 0].hist(x, bottom= 1)
axs[1, 1].hist(y, orientation="horizontal", bottom =1)
axs[1, 1].set_position(pos=[0.42, 0.125, 0.515, 0.515], which= 'original')

plt.show()
df.corr()