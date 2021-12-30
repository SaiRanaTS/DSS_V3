import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import xlrd
import numpy as np
from functools import reduce
from matplotlib.animation import FuncAnimation
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from matplotlib import transforms
from matplotlib.patches import Circle
import time
import Ship
from matplotlib.widgets import Button

x1 = [100,200,300,400,500]
y1 = [110,429,380,500,100]

x2 = [10,20,30,40,50]
y2 = [18,33,22,10,3]

r = np.arange(0, 2, 0.01)
theta = 2 * np.pi * r

fig = plt.figure(constrained_layout=True,figsize=(12,8),facecolor='black')
gs = GridSpec(3, 3, figure=fig)
plt.subplots_adjust(left=0.06, right=0.95, top=0.9, bottom=0.1, hspace=0.5)

Ship_number = 3

# load data Simulation_Data/F5R2.xlsx
path = 'Simulation_Data/F5R2.xlsx'  # D1R2, D2R1-2, F1R1-2, F4R1-5, F5R1-4
wb = xlrd.open_workbook(filename=path)  # 打开文件
ov_names = ['Ulstein', 'SULA', 'HEROY', 'Haram']
ov_data = wb.sheet_by_name(ov_names[Ship_number-1])  # 0-3
tv1_data = wb.sheet_by_name('Hannara')
tv2_data = wb.sheet_by_name('Stavangerfjord')
tv3_data = wb.sheet_by_name('UNI')
tv4_data = wb.sheet_by_name('Frigat 1')
tv5_data = wb.sheet_by_name('Frigat 2')

ax1 = fig.add_subplot(gs[0:2, 0:3])
ax2 = fig.add_subplot(gs[-1, 0])
ax3 = fig.add_subplot(gs[-1, -2],polar="true")


def plot_plor_axis():# for object
    ax3.set_theta_zero_location("N")
    ax3.set_theta_direction(-1)
    ax3.set_yticklabels([])
    ax3.set_ylim(0, 1)
    R0 = [0, 1]
    theta0 = np.deg2rad([355, 355])
    theta1 = np.deg2rad([5, 5])
    theta2 = np.deg2rad([67, 67])
    theta3 = np.deg2rad([112.5, 112.5])
    theta4 = np.deg2rad([210, 210])
    theta5 = np.deg2rad([247.5, 247.5])
    ax3.plot(theta0,R0, theta1, R0, theta2, R0,theta3, R0,theta4, R0,theta5, R0, lw=1,color = "red")
    ax3.grid(True)

ax6 = fig.add_subplot(gs[-1, -1])

axButton2 = plt.axes([0.1,0.01,0.1,0.05]) # left pos, bottom pos , width, height
axButton3 = plt.axes([0.4,0.01,0.1,0.05]) # left pos, bottom pos , width, height
axButton4 = plt.axes([0.8,0.01,0.1,0.05]) # left pos, bottom pos , width, height

globvar = 0
globvar1 = 0
globvar2 = 0

def return_1(event):
    global globvar
    globvar +=1
    print(p)
    return p

def return_2(event):
    global globvar1
    globvar1 +=1
    print(p)
    return p

def return_3(event):
    global globvar2
    globvar2 +=1
    print(p)
    return p
p = 0

btn2 = Button(ax = axButton2,label = 'Path',color='teal',hovercolor='tomato')
btn3 = Button(ax = axButton3,label = 'View Change',color='teal',hovercolor='tomato')
btn4 = Button(ax = axButton4,label = 'Ship info',color='teal',hovercolor='tomato')


btn2.on_clicked(return_1)
btn3.on_clicked(return_2)
btn4.on_clicked(return_3)



x = [0, -24]
y = [0, 4088]
ax1.plot(x[0], y[0], c='green', marker='o', markersize=8)
ax1.plot(x[1], y[1], c='red', marker='o', markersize=8)

fig.suptitle("Decision Support Systems v3.0",color = 'white')

# trajectory data
origin_x = 362024.07992
origin_y = 6918869.62932
time_frame = []
cri_1 = []
cri_2 = []
cri_3 = []
cri_4 = []
cri_5 = []

ma_time = []
ma_cri = []

dcpa_1 = []
dcpa_2 = []
dcpa_3 = []
dcpa_4 = []
dcpa_5 = []

ov_x, ov_y = [], []
tv1_x, tv1_y = [], []
tv2_x, tv2_y = [], []
tv3_x, tv3_y = [], []
tv4_x, tv4_y = [], []
tv5_x, tv5_y = [], []
ov_heading, ov_spd, ov_turn = [], [], []
tv1_heading, tv1_spd, tv1_turn = [], [], []
tv2_heading, tv2_spd, tv2_turn = [], [], []
tv3_heading, tv3_spd, tv3_turn = [], [], []
tv4_heading, tv4_spd, tv4_turn = [], [], []
tv5_heading, tv5_spd, tv5_turn = [], [], []
ln_ov, = ax1.plot([], [], 'g-', animated=False, alpha=0.3)
ln_tv1, = ax1.plot([], [], 'r-', animated=False, alpha=0.15)
ln_tv2, = ax1.plot([], [], 'orange', animated=False, alpha=0.15)
ln_tv3, = ax1.plot([], [], 'c', animated=False, alpha=0.15)
ln_tv4, = ax1.plot([], [], 'blue', animated=False, alpha=0.15)
ln_tv5, = ax1.plot([], [], 'yellow', animated=False, alpha=0.15)


# time_template = 'time: %.2fs'
time = []
time_text = ax1.text(100, 100, '', transform=ax1.transAxes, color='black')

def str2float(s):
    def str2num(s):
        return {str(x): x for x in range(10)}[s]

    l = s.split('.')
    s = s.replace('.', '')
    num = reduce(lambda a, b: a * 10 + b, map(str2num, s))
    return num / (10 ** len(l[-1])) if len(l) == 2 else num / 1

def moving_avg (values, window):
    weights = np.repeat(1.0,window)/window
    smas = np.convolve(values,weights)
    start = 0
    n = len(smas)
    interval = 1
    l = np.arange(start, interval * n, interval)
    pz = smas[:-12]
    pl = l[:-12]
    return pz, pl

def frame_str(frame,tvx,tvy,tvh,tvs,tvdata):
    #print('ppp')
    tvx.append(str2float(tvdata.row_values(frame)[4]) - origin_x)
    tvy.append(str2float(tvdata.row_values(frame)[5]) - origin_y)
    tvh.append(str2float((tvdata.row_values(frame)[1])))
    tvs.append(str2float(tvdata.row_values(frame)[3]))
    return

def frame_str_os(frame,osx,osy,osh,oss,osdata):
    #print('ppp')
    osx.append(str2float(osdata.row_values(frame)[10]) - origin_x)
    osy.append(str2float(osdata.row_values(frame)[11]) - origin_y)
    osh.append(str2float(osdata.row_values(frame)[1]))
    oss.append(str2float(osdata.row_values(frame)[5]))
    return

def plot_ts(vsl_heading,tv_x,tv_y,clor):

    tv_mk_rtt = transforms.Affine2D().rotate_deg(-vsl_heading)
    def_marker = Path([[-0.005, -0.02], [0.005, -0.02], [0.005, 0.01], [0, 0.02], [-0.005, 0.01], [0, 0], ],
                      [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    tv_mk = def_marker.transformed(tv_mk_rtt)
    ax1.scatter(tv_x, tv_y, marker=tv_mk, color=clor, s=15 ** 2, alpha=0.5)
    return

class ship_info:
    def __init__(self, no,name,xpos,ypos,lat,lon,speed,ori,head,l):
        #Own Ship Data
        self.ship_no = no
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.lat = lat
        self.lon = lon
        self.speed = speed
        self.ori = ori
        self.head = head
        self.l = l


def update(frame):

    ax1.clear()
    ax1.grid(alpha=0.2)
    ax1.set_xlabel('East (m)')
    ax1.set_ylabel('North (m)')
    ax1.set_facecolor("white")
    ax1.spines['bottom'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.yaxis.label.set_color('white')
    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    #ax1.legend()

    if globvar1 % 2:
        ax1.set_xlim([-4122, 6028])
        ax1.set_ylim([-400, 4675])

    ax2.clear()
    ax2.set_facecolor("white")
    ax2.set_ylim([0, 1])
    ax2.yaxis.label.set_color('white')
    ax2.xaxis.label.set_color('white')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')


    # Ship Marker Shape:
    def_marker = Path([[-0.005, -0.02], [0.005, -0.02], [0.005, 0.01], [0, 0.02], [-0.005, 0.01], [0, 0], ],
                      [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])

    #-----------------------------------------------------------------------------------------------------------------#
    frame_str_os(frame, ov_x, ov_y, ov_heading, ov_spd, ov_data)
    frame_str(frame,tv1_x,tv1_y,tv1_heading,tv1_spd,tv1_data)
    frame_str(frame, tv2_x, tv2_y, tv2_heading, tv2_spd, tv2_data)
    frame_str(frame, tv3_x, tv3_y, tv3_heading, tv3_spd, tv3_data)
    frame_str(frame, tv4_x, tv4_y, tv4_heading, tv4_spd, tv4_data)
    frame_str(frame, tv5_x, tv5_y, tv5_heading, tv5_spd, tv5_data)

    ov_mk_rtt = transforms.Affine2D().rotate_deg(-ov_heading[-1])

    os = ship_info(1,"OS1",ov_x[-1],ov_y[-1],3000,4000,ov_spd[-1],ov_heading[-1],40,0.0269978)
    ts1 = ship_info(1,"Hannara",tv1_x[-1],tv1_y[-1],1000,2000,tv1_spd[-1],tv1_heading[-1],30,0.0269978)
    ts2 = ship_info(2, "Stavangerfjord", tv2_x[-1], tv2_y[-1], 1000, 2000, tv2_spd[-1], tv2_heading[-1], 30, 0.0269978)
    ts3 = ship_info(3, "UNI", tv3_x[-1], tv3_y[-1], 1000, 2000, tv3_spd[-1], tv3_heading[-1], 30, 0.0269978)
    ts4 = ship_info(4, "Frigat 1", tv4_x[-1], tv4_y[-1], 1000, 2000, tv4_spd[-1], tv4_heading[-1], 30, 0.0269978)
    ts5 = ship_info(5, "Frigat 2", tv5_x[-1], tv5_y[-1], 1000, 2000, tv5_spd[-1], tv5_heading[-1], 30, 0.0269978)


    ship1 = Ship.ship(ts1.ship_no,ts1.name,ts1.xpos,ts1.ypos,ts1.lat,ts1.lon,ts1.speed,ts1.ori,ts1.head,ts1.l,os.ship_no,os.name,os.xpos,os.ypos,os.lat,os.lon,os.speed,os.ori,os.head,os.l)
    ship2 = Ship.ship(ts2.ship_no,ts2.name,ts2.xpos,ts2.ypos,ts2.lat,ts2.lon,ts2.speed,ts2.ori,ts2.head,ts2.l,os.ship_no,os.name,os.xpos,os.ypos,os.lat,os.lon,os.speed,os.ori,os.head,os.l)
    ship3 = Ship.ship(ts3.ship_no,ts3.name,ts3.xpos,ts3.ypos,ts3.lat,ts3.lon,ts3.speed,ts3.ori,ts3.head,ts3.l,os.ship_no,os.name,os.xpos,os.ypos,os.lat,os.lon,os.speed,os.ori,os.head,os.l)
    ship4 = Ship.ship(ts4.ship_no,ts4.name,ts4.xpos,ts4.ypos,ts4.lat,ts4.lon,ts4.speed,ts4.ori,ts4.head,ts4.l,os.ship_no,os.name,os.xpos,os.ypos,os.lat,os.lon,os.speed,os.ori,os.head,os.l)
    ship5 = Ship.ship(ts5.ship_no,ts5.name,ts5.xpos,ts5.ypos,ts5.lat,ts5.lon,ts5.speed,ts5.ori,ts5.head,ts5.l,os.ship_no,os.name,os.xpos,os.ypos,os.lat,os.lon,os.speed,os.ori,os.head,os.l)

    ax1.text(ov_x[-1] + 100, ov_y[-1], f'Own Ship : Ulstein', fontsize=10, color='black')

    #-------------------------------------- Domain Implementation------------------------------------------------------

    ov_mk = def_marker.transformed(ov_mk_rtt)
    ax1.scatter(ov_x[-1], ov_y[-1], marker=ov_mk, color='black', s=15 ** 2, alpha=0.5)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------
    circle0 = Circle([1, 1], 2)
    cir_path0 = circle0.get_path()
    t0_crk = cir_path0.transformed(ov_mk_rtt)
    skl =40
    ax1.scatter(ov_x[-1], ov_y[-1], marker=t0_crk, facecolors='none', edgecolors='g', s=skl ** 2.7, alpha=0.7)
    ax1.scatter(ov_x[-1], ov_y[-1], marker=t0_crk, facecolors='none', edgecolors='black', s=skl ** 3.0, alpha=0.4,linestyle='dashed')

    plot_ts(tv1_heading[-1],tv1_x[-1],tv1_y[-1],'red')
    plot_ts(tv2_heading[-1],tv2_x[-1],tv2_y[-1],'red')
    plot_ts(tv3_heading[-1],tv3_x[-1],tv3_y[-1],'red')
    plot_ts(tv4_heading[-1],tv4_x[-1],tv4_y[-1],'red')
    plot_ts(tv5_heading[-1],tv5_x[-1],tv5_y[-1],'red')

    if globvar2 % 2:
        ax1.text(tv1_x[-1] + 100, tv1_y[-1],f'T{ts1.ship_no}: {ts1.name}\n CRI :{round(ship1.cri,3)}\n Alpha OT :{round(ship1.alpha_ot,3)}\n DCPA :{round(ship1.DCPA,3)}\n TCPA :{round(ship1.TCPA,3)}\n D :{round(ship1.d,3)} ', fontsize=10, color='black')
        ax1.text(tv2_x[-1] + 100, tv2_y[-1], f'T{ts2.ship_no}: {ts2.name}\n CRI :{round(ship2.cri,3)}\n Alpha OT :{round(ship2.alpha_ot,3)}\n DCPA :{round(ship2.DCPA,3)}\n TCPA :{round(ship2.TCPA,3)}\n D :{round(ship2.d,3)} ', fontsize=10,color='black')
        ax1.text(tv3_x[-1] + 100, tv3_y[-1], f'T{ts3.ship_no}: {ts3.name}\n CRI :{round(ship3.cri,3)}\n Alpha OT :{round(ship3.alpha_ot,3)}\n DCPA :{round(ship3.DCPA,3)}\n TCPA :{round(ship3.TCPA,3)}\n D :{round(ship3.d,3)}', fontsize=10,color='black')
        ax1.text(tv4_x[-1] + 100, tv4_y[-1], f'T{ts4.ship_no}: {ts4.name}\n CRI :{round(ship4.cri,3)}\n Alpha OT :{round(ship4.alpha_ot,3)}\n DCPA :{round(ship4.DCPA,3)}\n TCPA :{round(ship4.TCPA,3)}\n D :{round(ship4.d,3)}', fontsize=10,color='black')
        ax1.text(tv5_x[-1] + 100, tv5_y[-1], f'T{ts5.ship_no}: {ts5.name}\n CRI :{round(ship5.cri,3)}\n Alpha OT :{round(ship5.alpha_ot,3)}\n DCPA :{round(ship5.DCPA,3)}\n TCPA :{round(ship5.TCPA,3)}\n D :{round(ship5.d,3)}', fontsize=10,color='black')
    else:
        ax1.text(tv1_x[-1] + 100, tv1_y[-1],f'T{ts1.ship_no}: {ts1.name}', fontsize=10, color='black')
        ax1.text(tv2_x[-1] + 100, tv2_y[-1], f'T{ts2.ship_no}: {ts2.name}', fontsize=10, color='black')
        ax1.text(tv3_x[-1] + 100, tv3_y[-1], f'T{ts3.ship_no}: {ts3.name}', fontsize=10, color='black')
        ax1.text(tv4_x[-1] + 100, tv4_y[-1], f'T{ts4.ship_no}: {ts4.name}', fontsize=10, color='black')
        ax1.text(tv5_x[-1] + 100, tv5_y[-1], f'T{ts5.ship_no}: {ts5.name}', fontsize=10, color='black')

    if globvar % 2:
        ax1.plot(ov_x,ov_y)
        ax1.plot(tv1_x,tv1_y)
        ax1.plot(tv2_x, tv2_y)
        ax1.plot(tv3_x, tv3_y)
        ax1.plot(tv4_x, tv4_y)
        ax1.plot(tv5_x, tv5_y)

    time_frame.append(frame)
    cri_1.append(round(ship1.cri,1))
    cri_2.append(round(ship2.cri,1))
    cri_3.append(round(ship3.cri,1))
    cri_4.append(round(ship4.cri,1))
    cri_5.append(round(ship5.cri,1))

    ln_ov.set_data(ov_x, ov_y)
    ln_tv1.set_data(tv1_x, tv1_y)
    ln_tv2.set_data(tv2_x, tv2_y)
    ln_tv3.set_data(tv3_x, tv3_y)
    ln_tv4.set_data(tv4_x, tv4_y)
    ln_tv5.set_data(tv5_x, tv5_y)
    time.append(ov_data.row_values(frame)[0])
    time_text.set_text(time[-1])

    #Moving Average Calculation
    ma1 = moving_avg(cri_1,12)
    ma2 = moving_avg(cri_2, 12)
    ma3 = moving_avg(cri_3, 12)
    ma4 = moving_avg(cri_4, 12)
    ma5 = moving_avg(cri_5, 12)




    ax2.plot(ma1[1],ma1[0], label="TS 1")
    ax2.plot(ma2[1], ma2[0], label="TS 2")
    ax2.plot(ma3[1], ma3[0], label="TS 3")
    ax2.plot(ma4[1], ma4[0], label="TS 4")
    ax2.plot(ma5[1], ma5[0], label="TS 5")

    #ax2.plot(time_frame, cri_1,label="TS 1")
    #ax2.plot(time_frame, cri_2,label="TS 2")
    #ax2.plot(time_frame, cri_3,label="TS 3")
    #ax2.plot(time_frame, cri_4,label="TS 4")
    #ax2.plot(time_frame, cri_5,label="TS 5")

    ax2.legend(bbox_to_anchor=(0., 1.02, 1.0, .102), loc='lower left',
                      ncol=3, mode="expand", borderaxespad=0.)
    ax3.clear()
    ax3.set_facecolor("white")
    ax3.yaxis.label.set_color('white')
    ax3.xaxis.label.set_color('white')
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    plot_plor_axis()
    ax3.scatter(np.deg2rad(round(ship1.alpha_ot,3)),round(ship1.d,3))
    ax3.scatter(np.deg2rad(round(ship2.alpha_ot,3)),round(ship2.d,3))
    ax3.scatter(np.deg2rad(round(ship3.alpha_ot,3)),round(ship3.d,3))
    ax3.scatter(np.deg2rad(round(ship4.alpha_ot,3)),round(ship4.d,3))
    ax3.scatter(np.deg2rad(round(ship5.alpha_ot,3)),round(ship5.d,3))

    return ln_ov, ln_tv1, ln_tv2, ln_tv3, ln_tv4, ln_tv5, time_text,

ani = FuncAnimation(fig, update, frames=np.arange(1, 900, 1), blit=True, interval=10, repeat=False)  # interval (ms)

class UnsizedMarker(MarkerStyle):
    def _set_custom_marker(self, path):
        self._transform = transforms.IdentityTransform()
        self._path = path
plt.show()