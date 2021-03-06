$fn=150;
stackX=5.5;
stackY=88;
stackZ=45;
stackDistance=101.5;
T=0.05;

module support(D1,H1, D1H, D2, H2, D2H, offsetval, tolerance)
{
    difference()
    {
        union(){
            cylinder(r=(D1/2), h=H1, center=false);
    translate([offsetval,0,H1])cylinder(r=(D2/2), h=H2, center=false);
             translate([0,0,H1-(H1+H2)/6])
hull()
        {//Connecition
         cylinder(r=(D1/2), h=(H1+H2)/3, center=false);
          translate([offsetval,0,0])cylinder(r=D2/2, h=(H1+H2)/3, center=false);   
            
        }    
            }
            //Holes
        cylinder(r=D1H/2+tolerance, h=3*H1, center=false);
         translate([offsetval,0,H1-(H1+H2)/2])cylinder(r=D2H/2+tolerance, h=3*H2, center=false);
    }
   
}

module washer(D)
{
    difference()
    {
        cylinder(r=3*D/2, h=1, center=false);
        cylinder(r=D/2+0.1*D, h=1, center=false);

    }
}

module SUB_stackFrame(stackX, stackY, stackZ)
{
    //Hole space is 17.5
    cube([stackX, stackY, stackZ], center=true);
    translate([64.5,0,0])cube([stackX, stackY, stackZ], center=true);
    translate([64.5/2,0,+stackZ/4])cube([64.5, stackX, stackZ/2], center=true);
    

}

module stack()
{
difference()

{
    SUB_stackFrame(stackX, stackY, stackZ);
for (i = [0: 1: 4]) {
translate([0,stackY/2-9-1/2-i*17.5,stackZ/2-20])cylinder(r=2/2-2*T, h=25);
translate([64.5,stackY/2-9-1/2-i*17.5,stackZ/2-20])cylinder(r=2/2-2*T, h=25);

translate([0,stackY/2-9-1/2-i*17.5,-stackZ/2-20])cylinder(r=2/2-2*T, h=25);
translate([64.5,stackY/2-9-1/2-i*17.5,-stackZ/2-20])cylinder(r=2/2-2*T, h=25);
    
}
translate([-10,0,-5])rotate([90,00,90])linear_extrude(height = 90)scale([1,0.3,1])circle(r=stackY*1/3, center=true);

}
}


//stack();



/*translate([])rotate([0,90,0])
hull()
{
    cylinder(r=stackY/5,h=2*stackX);
    translate([stackZ/2-stackY/5,0,0])cylinder(r=stackY/5,h=2*stackX);
    
}*/

support(2,25, 2, 5, 15.75);
translate([35,0,0])support(2,25, 2, 5, 20);
translate([35,35,0])support(2,25, 2, 5, 14.5);
translate([0,35,0])support(2,25, 2, 5, 15.75);

//washer(3);
//support(3,10, 0, 0, 0,0.3);
translate([35,0,0])support(2.5,0, 2.5, 15, 15, 0.0);
//translate([35,35,0])support(3,40, 0, 0, 0);
//translate([0,35,0])support(3,40, 0, 0, 0);
stack();