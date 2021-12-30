import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
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

# background
img = plt.imread("bpo.png")
fig, ax = plt.subplots()
fig.set_size_inches(12, 8)
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
ax.imshow(img, extent=[-4122, 6028, -400, 4675], alpha=0.96)
plt.xlim([-4122, 6028])
plt.ylim([-400, 4675])
plt.xlabel('East (m)')
plt.ylabel('North (m)')
plt.grid(alpha=0.2)
ax.set_title(u"|Simulation From AIS Data|")
ax.legend()

# departure and arrival
x = [0, -24]
y = [0, 4088]
plt.plot(x[0], y[0], c='green', marker='o', markersize=8)
plt.plot(x[1], y[1], c='red', marker='o', markersize=8)

# trajectory data
origin_x = 362024.07992
origin_y = 6918869.62932
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
ln_ov, = ax.plot([], [], 'g-', animated=False, alpha=0.3)
ln_tv1, = ax.plot([], [], 'r-', animated=False, alpha=0.15)
ln_tv2, = ax.plot([], [], 'orange', animated=False, alpha=0.15)
ln_tv3, = ax.plot([], [], 'c', animated=False, alpha=0.15)
ln_tv4, = ax.plot([], [], 'blue', animated=False, alpha=0.15)
ln_tv5, = ax.plot([], [], 'yellow', animated=False, alpha=0.15)

# time_template = 'time: %.2fs'
time = []
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, color='white')

def str2float(s):
    def str2num(s):
        return {str(x): x for x in range(10)}[s]

    l = s.split('.')
    s = s.replace('.', '')
    num = reduce(lambda a, b: a * 10 + b, map(str2num, s))
    return num / (10 ** len(l[-1])) if len(l) == 2 else num / 1

def frame_str(frame,tvx,tvy,tvh,tvs,tvdata):
    print('ppp')
    tvx.append(str2float(tvdata.row_values(frame)[4]) - origin_x)
    tvy.append(str2float(tvdata.row_values(frame)[5]) - origin_y)
    tvh.append(str2float((tvdata.row_values(frame)[1])))
    tvs.append(str2float(tvdata.row_values(frame)[3]))
    return

def frame_str_os(frame,osx,osy,osh,oss,osdata):
    print('ppp')
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
    plt_tv_mk = ax.scatter(tv_x, tv_y, marker=tv_mk, color=clor, s=15 ** 2, alpha=0.5)
    return plt_tv_mk

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

    plt_ov_txt = plt.text(ov_x[-1] + 100, ov_y[-1], f'Own Ship : Ulstein', fontsize=10, color='white')

    #-------------------------------------- Domain Implementation------------------------------------------------------

    ov_mk = def_marker.transformed(ov_mk_rtt)
    plt_ov_mk = ax.scatter(ov_x[-1], ov_y[-1], marker=ov_mk, color='white', s=15 ** 2, alpha=0.5)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------
    circle0 = Circle([1, 1], 2)
    cir_path0 = circle0.get_path()
    t0_crk = cir_path0.transformed(ov_mk_rtt)
    skl =10
    plt_t0_cir = ax.scatter(ov_x[-1], ov_y[-1], marker=t0_crk, facecolors='none', edgecolors='g', s=skl ** 2.7, alpha=0.7)
    plt_t00_cir = ax.scatter(ov_x[-1], ov_y[-1], marker=t0_crk, facecolors='none', edgecolors='white', s=skl ** 3.0, alpha=0.4,linestyle='dashed')

    sh1 = plot_ts(tv1_heading[-1],tv1_x[-1],tv1_y[-1],'red')
    plt_tv_txt = ax.text(tv1_x[-1] + 100, tv1_y[-1],f'T{ts1.ship_no}: {ts1.name}\n CRI :{round(ship1.cri,3)}\n Alpha OT :{round(ship1.alpha_ot,3)}\n DCPA :{round(ship1.DCPA,3)}\n TCPA :{round(ship1.TCPA,3)}\n D :{round(ship1.d,3)}   ', fontsize=10, color='white')

    sh2 = plot_ts(tv2_heading[-1],tv2_x[-1],tv2_y[-1], 'red')
    plt_tv2_txt = plt.text(tv2_x[-1] + 100, tv2_y[-1], f'T{ts2.ship_no}: {ts2.name}\n CRI :{round(ship2.cri,3)}\n Alpha OT :{round(ship2.alpha_ot,3)}\n DCPA :{round(ship2.DCPA,3)}\n TCPA :{round(ship2.TCPA,3)}\n D :{round(ship2.d,3)} ', fontsize=10,color='white')

    sh3 = plot_ts(tv3_heading[-1], tv3_x[-1], tv3_y[-1], 'red')
    plt_tv3_txt = plt.text(tv3_x[-1] + 100, tv3_y[-1], f'T{ts3.ship_no}: {ts3.name}\n CRI :{round(ship3.cri,3)}\n Alpha OT :{round(ship3.alpha_ot,3)}\n DCPA :{round(ship3.DCPA,3)}\n TCPA :{round(ship3.TCPA,3)}\n D :{round(ship3.d,3)}', fontsize=10,color='white')

    sh4 = plot_ts(tv4_heading[-1], tv4_x[-1], tv4_y[-1], 'red')
    plt_tv4_txt = plt.text(tv4_x[-1] + 100, tv4_y[-1], f'T{ts4.ship_no}: {ts4.name}\n CRI :{round(ship4.cri,3)}\n Alpha OT :{round(ship4.alpha_ot,3)}\n DCPA :{round(ship4.DCPA,3)}\n TCPA :{round(ship4.TCPA,3)}\n D :{round(ship4.d,3)}', fontsize=10,color='white')

    sh5 = plot_ts(tv5_heading[-1], tv5_x[-1], tv5_y[-1], 'red')
    plt_tv5_txt = plt.text(tv5_x[-1] + 100, tv5_y[-1], f'T{ts5.ship_no}: {ts5.name}\n CRI :{round(ship5.cri,3)}\n Alpha OT :{round(ship5.alpha_ot,3)}\n DCPA :{round(ship5.DCPA,3)}\n TCPA :{round(ship5.TCPA,3)}\n D :{round(ship5.d,3)}', fontsize=10,color='white')

    ln_ov.set_data(ov_x, ov_y)
    ln_tv1.set_data(tv1_x, tv1_y)
    ln_tv2.set_data(tv2_x, tv2_y)
    ln_tv3.set_data(tv3_x, tv3_y)
    ln_tv4.set_data(tv4_x, tv4_y)
    ln_tv5.set_data(tv5_x, tv5_y)
    time.append(ov_data.row_values(frame)[0])
    time_text.set_text(time[-1])

    return sh5,sh4,sh2,sh3,plt_tv_txt,sh1,plt_t00_cir,ln_ov, ln_tv1, ln_tv2, ln_tv3,plt_ov_txt, ln_tv4, ln_tv5, time_text, plt_ov_mk, plt_tv2_txt, plt_tv3_txt, plt_tv4_txt, plt_tv5_txt,plt_t0_cir,

class UnsizedMarker(MarkerStyle):
    def _set_custom_marker(self, path):
        self._transform = transforms.IdentityTransform()
        self._path = path



ani = FuncAnimation(fig, update, frames=np.arange(1, 900, 1), blit=True, interval=10, repeat=False)  # interval (ms)
#mngr = plt.get_current_fig_manager()
#mngr.window.wm_geometry("+0+0")
plt.show()