ls1 = [] 
ls2 = []
#key val in seperate lines
for line in lst:
    ll = len(line)

   # print(ll)

    if (ll%2==0  and ll>0) :
        flag = True

        for word in line  :
            if flag is True :

                #print(word,end=":")
                ls1.append(word)
                flag =False
                continue

            if flag is False :

                #print(word)
                ls2.append(word)
                flag = True 
                continue    



        

    elif(ll%2==1 and ll>0) :
        flag = True
        cnt = 1 

        if(ll==1) :
            #print(line[0],end=":")
            print(" ")
            ls1.append(line[0])
            ls2.append(" ")
        else :
            for word in line  :
                if(cnt ==1) :
                    ls1.append(word)
                    ls2.append(" ")
                else :
                    if flag is True :
                        #print(word,end=":")
                        ls1.append(word)
                
                        flag =False
                        continue

                    if flag is False :
                        #print(word,end=":")
                        ls2.append(word)
                        flag = True 
                        continue
                cnt+=1     


# print(ls1)
# print(ls2)


ou = dict(zip(ls1, ls2))

#print(str(ou))


json_object = json.dumps(ou, indent = 4) 
print(json_object)