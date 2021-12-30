import math
import numpy as np

def motion_parameters(osx, osy, os_theta,os_speed, tsx,tsy, ts_theta, ts_speed):

    #Intermidiate Motion Parameters
    vox = os_speed * math.sin(math.radians(os_theta))
    voy = os_speed * math.cos(math.radians(os_theta))
    vtx = ts_speed * math.sin(math.radians(ts_theta))
    vty = ts_speed * math.cos(math.radians(ts_theta))
    v_x = vtx - vox
    v_y = vty - voy
    x_ot = tsx - osx
    y_ot = tsy - osy

   #print(f'OS X :{osx}\nOS Y :{osy}\n\nOS speed :{os_speed}\nOS theta :{os_theta}\nTS X :{tsx}\nTS Y :{tsy}\nTS Speed :{ts_speed}\nTS Theta :{ts_theta}')
    #print(f'Vox :{vox}\nVoy Y :{voy}\n\nVtx :{vtx}\nVty :{vty}\nVx :{v_x}\nVy :{v_y}\nXot :{x_ot}\nYot :{y_ot}')




    #Relative speed
    if os_speed == 0:
        os_speed = 0.0001
    else:
        os_speed = os_speed
    v_ot = os_speed * math.sqrt(1 + (ts_speed / os_speed) ** 2 - 2 * (ts_speed / os_speed) * math.cos(os_theta - ts_theta))

    #theta_ot
    if v_x >= 0 and v_y >= 0:
        theta_ot = math.atan(v_x/v_y)
    elif v_x <0 and v_y < 0:
        theta_ot = math.atan(v_x/v_y) + 180
    elif v_x >= 0 and v_y < 0:
        theta_ot = math.atan(v_x/v_y) + 180
    elif v_x < 0 and v_y >=0:
        theta_ot = math.atan(v_x/v_y) + 360

    #alpha_t
    if x_ot>= 0 and y_ot >= 0:
        alpha_t = math.degrees(math.atan(x_ot/y_ot))
    elif x_ot < 0 and y_ot < 0:
        alpha_t = math.degrees(math.atan(x_ot/y_ot)) + 180
    elif x_ot >= 0 and y_ot < 0:
        alpha_t = math.degrees(math.atan(x_ot/y_ot)) + 180
    elif x_ot < 0 and y_ot >= 0:
        alpha_t = math.degrees(math.atan(x_ot/y_ot)) + 360

    #alpha_ot
    alpha_ot = alpha_t - os_theta
    if alpha_ot < 0:
        alpha_ot = alpha_ot + 360
    elif alpha_ot > 360:
        alpha_ot = alpha_ot - 360

    # Distance between
    d = math.sqrt((tsx - osx)**2 + (tsy - osy)**2)  * 0.000539957

    #print("D :",d)

    #DCPA
    DCPA = d * math.sin(math.radians(theta_ot-alpha_t-180))


    #TCPA
    TCPA = (d*math.cos(math.radians(theta_ot-alpha_t-180)))/v_ot

    return v_ot, theta_ot, alpha_t, alpha_ot, d, DCPA, TCPA # Relative Speed, Theta_OT, Alpha_t, Alpha_OT, Diatnce between, DCPA, TCPA



def membership_fun(DCPA,alpha_ot,TCPA,d,v_ot,l,theta_t,theat_o):

    if alpha_ot >= 355 and alpha_ot <= 360:
        d1 = 1.1
        d2 = 2.2

    elif alpha_ot >= 0 and alpha_ot < 67.5:
        d1 = 1.1
        d2 = 2.2
    elif alpha_ot >= 67.5 and alpha_ot < 112.5:
        d1 = 1.0
        d2 = 2.0
    elif alpha_ot >= 112.5 and alpha_ot < 247.5:
        d1 = 0.6
        d2 = 1.2
    else: #alpha_ot >= 247.5 and alpha_ot < 355:
        d1 = 0.9
        d2 = 1.8

    #------- u of DCPA --------

    if abs(DCPA) < d1:
        u_DCPA = 1
    elif d2 <= abs(DCPA) <=d2:
        u_DCPA = ((d2 - abs(DCPA))/(d2-d1))**2
    else:
        u_DCPA = 0

    #------- u of TCPA - t1 nd t2 --------

    if DCPA <= d1:
        t1 = (math.sqrt(abs(d1**2 - DCPA**2))/v_ot)
    elif DCPA >d1:
        t1 = ((d1 - DCPA)/v_ot)

    t2 = math.sqrt(abs(d2**2 - DCPA**2))/v_ot

    #------------- u_TCPA -----------

    if 0 <= abs(TCPA) <= t1:
        u_TCPA = 1
    elif t1 < abs(TCPA)<= t2:
        u_TCPA = ((t2 - abs(TCPA))/(t2 - t1))**2
    elif abs(TCPA)> t2:
        u_TCPA = 0


    #--------- D1 and D2 -----------
    L = 0.0269978
    D1 = 12 * L

    R = 1.7 * math.cos(alpha_ot - 19) + math.sqrt(4.4 + 2.89*(math.cos(alpha_ot-19))**2)

    D2 = R

    #----- u_D ------

    if 0 < d and d< D1:
        u_D = 1
    elif D1 <= d <= D2:
        u_D = ((D2 - d)/(D2-D1))**2
    elif d > D2:
        u_D = 0


    #----------- Alpha ot --------------

    u_alpha_ot = 0.5 * (math.cos(alpha_ot - 19) + math.sqrt((440/289) + math.cos(alpha_ot - 19)**2)) - (5/17)

    K = 2.0
    #membership function for K
    u_K = ((1)/(1+((2)/K*(math.sqrt(K**2 + 1 + 2*K*math.sin(abs(theta_t-theat_o)))))))



    #print("U_DCPA :", round(u_DCPA,3))
    #print("U_TCPA :", round(u_TCPA,3))
    #print("U_D :", round(u_D,3))
    #print("U_AlphaOT :", round(u_alpha_ot,3))


    return u_DCPA,u_TCPA,u_D,u_alpha_ot,u_K

def cri_function(u_DCPA,u_TCPA,u_D,u_alpha_ot,u_K):

    UF = np.array([[u_DCPA], [u_TCPA], [u_D], [u_alpha_ot], [u_K]])
    WF = np.array([[float(0.4), float(0.367), float(0.133), float(0.067), float(0.033)]])
    CRF = WF.dot(UF)
    CRF_rn = round(CRF[0][0], 3)

    return CRF_rn


class ship:
    def __init__(self,ship_no,name,xpos,ypos,lat,lon,speed,ori,head,l,os_ship_no,os_name,os_xpos,os_ypos,os_lat,os_lon,os_speed,os_ori,os_head,os_l):

        #Own Ship Data

        self.os_ship_no = os_ship_no
        self.os_name = os_name
        self.os_xpos = os_xpos
        self.os_ypos = os_ypos
        self.os_lat = os_lat
        self.os_lon = os_lon
        self.os_speed = os_speed
        self.os_ori = os_ori
        self.os_head = os_head
        self.os_l = os_l



        #Target Ship Data
        self.ship_no = ship_no
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.lat = lat
        self.lon = lon
        self.speed = speed
        self.ori = ori
        self.head = head
        self.l = l

        #Motion Parameters
        self.mp = motion_parameters(self.os_xpos,self.os_ypos,self.os_ori,self.os_speed,self.xpos,self.ypos,self.ori,self.speed)

        self.vot = self.mp[0]
        self.theta_ot = self.mp[1]
        self.alpha_t = self.mp[2]
        self.alpha_ot = self.mp[3]
        self.d = self.mp[4]
        self.DCPA = self.mp[5]
        self.TCPA = self.mp[6]

        #Memebership Function
        self.mf = membership_fun(self.DCPA,self.alpha_ot,self.TCPA,self.d,self.vot,self.l,self.ori,self.os_ori)
        self.u_DCPA = self.mf[0]
        self.u_TCPA = self.mf[1]
        self.u_D = self.mf[2]
        self.u_alpha_ot = self.mf[3]
        self.u_K = self.mf[4]

        #CRI Index

        self.cri = cri_function(self.u_DCPA,self.u_TCPA,self.u_D,self.u_alpha_ot,self.u_K)






#-----------OS------------
os_no = 1
os_name = "OS1"
os_x = 0
os_y = 0
os_lat = 3000
os_lon = 4000
os_speed = 15
os_ori = 50
os_head = 40
os_length = 50 * 0.000539957



#-----------TS------------
ts_no = 2
ts_name = "PSV 001"
ts_x = 79.73
ts_y = 21.77
ts_lat = 1000
ts_lon = 2000
ts_speed = 15
ts_ori = 330
ts_head = 30
ts_length = 50 * 0.000539957

ship1 = ship(ts_no,ts_name,ts_x,ts_y,ts_lat,ts_lon,ts_speed,ts_ori,ts_head,ts_length,os_no,os_name,os_x,os_y,os_lat,os_lon,os_speed,os_ori,os_head,os_length)

#print(ship1.cri)

