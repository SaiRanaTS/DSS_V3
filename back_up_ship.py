import math
import numpy as np

def motion_parameters(osx, osy, os_theta,os_speed, tsx,tsy, ts_theta, ts_speed):

    #Intermidiate Motion Parameters
    vox = os_speed * math.sin(os_theta)
    voy = os_speed * math.cos(os_theta)
    vtx = ts_speed * math.sin(ts_theta)
    vty = ts_speed * math.cos(ts_theta)
    v_x = vtx - vox
    v_y = vty - voy
    x_ot = tsx - osx
    y_ot = tsy - osy

    #Relative speed
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
    d = math.sqrt((ts_x - os_x)**2 + (ts_y - os_y)**2)

    #DCPA
    DCPA = d * math.sin(theta_ot-alpha_t-180)

    #TCPA
    TCPA = (d*math.cos(theta_ot-alpha_t-180))/v_ot
    return v_ot, theta_ot, alpha_t, alpha_ot, d, DCPA, TCPA # Relative Speed, Theta_OT, Alpha_t, Alpha_OT, Diatnce between, DCPA, TCPA



def membership_fun(DCPA,alpha_ot,TCPA,d,v_ot,l,theta_t,theat_o):

    K = 2.0

    if 0<=alpha_ot<112.5:
        d1 = 1.1 -((0.2*alpha_ot)/180)
    elif 112.5<=alpha_ot<180:
        d1 =1.0 -((0.4*alpha_ot)/180)
    elif 180<=alpha_ot<247.5:
        d1 = 1.0 -((0.4*(360-alpha_ot))/180)
    elif 247.5 <=alpha_ot<=360:
        d1 = 1.1 - ((0.2*(360-alpha_ot))/180)

    d2 = K*d1

    if d2 < abs(DCPA):
        u_DCPA = 0
    elif d1 < abs(DCPA) <= d2:
        u_DCPA = 0.5 - 0.5*math.sin(((180)/(d2-d1))*(abs(DCPA)-((d1+d2)/2)))
    elif abs(DCPA) <= d1:
        u_DCPA = 1

    #D1 and D2 Calculation
    D1 = 12*l
    D2 = 1.7*math.cos(alpha_ot-19) + math.sqrt((4.4 + 2.89*(math.cos(alpha_ot-19))**2))

    #t1 and t2 calculation

    if DCPA <=D1:
        t1 = math.sqrt((D1**2)-(DCPA**2))/v_ot
    else:
        t1 = (D1-DCPA)/v_ot

    if DCPA <= D2:
        t2 = math.sqrt((D2**2)-(DCPA**2))/v_ot
    else:
        t2 = (D2-DCPA)/v_ot

    #membership function for TCPA
    if t2<abs(TCPA):
        u_TCPA = 0
    elif t1<abs(TCPA)<=t2:
        u_TCPA = ((t2-abs(TCPA))/(t2-t1))**2
    elif 0<=abs(TCPA)<t2:
        u_TCPA = 1

    #membership function for D
    if D2<d:
        u_D = 0
    elif D1 < d <= D2:
        u_D = ((D2-d)/(D2-D1))**2
    elif d <=D1:
        u_D = 1

    #membership function for alpha_ot
    print('alpha ot :',alpha_ot)
    u_alpha_ot = 0.5*(math.cos(alpha_ot-19) + math.sqrt((440/289) + math.pow(math.cos(alpha_ot-19), 2))) - (5/17)

    #membership function for K
    u_K = ((1)/(1+((2)/K*(math.sqrt(K**2 + 1 + 2*K*math.sin(abs(theta_t-theat_o)))))))


    print('u DCPA :',round(u_DCPA,2))
    print('u_TCPA :',round(u_TCPA,2))
    print('u_D :', round(u_D,2))
    print('u_alpha_ot :',round(u_alpha_ot,2))
    return u_DCPA,u_TCPA,u_D,u_alpha_ot,u_K

def cri_function(u_DCPA,u_TCPA,u_D,u_alpha_ot,u_K):

    UF = np.array([[u_DCPA], [u_TCPA], [u_D], [u_alpha_ot], [u_K]])
    WF = np.array([[float(0.4), float(0.367), float(0.133), float(0.067), float(0.033)]])
    CRF = WF.dot(UF)
    CRF_rn = round(CRF[0][0], 3)

    return CRF_rn

class oship:
    def __init__(self, ship_no,name,xpos,ypos,lat,lon,speed,ori,head,l):
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

class tship:
    def __init__(self,ship_no,name,xpos,ypos,lat,lon,speed,ori,head,l):
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
        self.mp = motion_parameters(os1.xpos,os1.ypos,os1.ori,os1.speed,self.xpos,self.ypos,self.ori,self.speed)
        self.vot = self.mp[0]
        self.theta_ot = self.mp[1]
        self.alpha_t = self.mp[2]
        self.alpha_ot = self.mp[3]
        self.d = self.mp[4]
        self.DCPA = self.mp[5]
        self.TCPA = self.mp[6]

        #Memebership Function
        self.mf = membership_fun(self.DCPA,self.alpha_ot,self.TCPA,self.d,self.vot,self.l,self.ori,os1.ori)
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
os_length = 50

os1 = oship(os_no,os_name,os_x,os_y,os_lat,os_lon,os_speed,os_ori,os_head,os_length)


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
ts_length = 50

ship1 = tship(ts_no,ts_name,ts_x,ts_y,ts_lat,ts_lon,ts_speed,ts_ori,ts_head,ts_length)

#print(ship1.cri)

