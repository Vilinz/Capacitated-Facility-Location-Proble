# Capacitated-Facility-Location-Proble



Suppose there are n facilities and m customers. We wish to choose: 

-  which of the n facilities to open 
-  the assignment of customers to facilities 
-  The objective is to minimize the sum of the opening cost and the assignment cost. 
-  The total demand assigned to a facility must not exceed its capacity. 

具体描述请看

https://blog.csdn.net/qq_36124194/article/details/85176717



数据集描述

There are currently 71 data files. The format of these data files is:

 

|J| |I|

s_1 f_1

s_2 f_2

  ...

s_|J| f_|J|

d_1 d_2 d_3 … d_|I|

c_{11} c_{12} c_{13} … c_{1|I|} 

c_{21} c_{22} c_{23} … c_{2|I|} 

   ...    ...    ...   ....

c_{|J|1} c_{|J|2} c_{|J|3} … c_{|J||I|} 

 

where:

 

|J| is the number of potential facility locations;

|I| is the number of customers;

s_j (j=1,...,|J|) is the capacity of facility j;

f_j (j=1,...,|J|) is the fixed cost of opening facility j;

d_i (i=1,...,|I|) is the demand of customer i;

c_{ji} (j=1,...,|J|), (i=1,...,|I|) is the cost of allocating all the demand of customer i to facility j.

 