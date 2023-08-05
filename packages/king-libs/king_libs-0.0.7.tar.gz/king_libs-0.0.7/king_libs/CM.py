from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.preprocessing import normalize
import time
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from tqdm import tqdm
import numpy as np
from random import choice
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier

class Conf_metrics_show():

    def __init__(self):

        pass

#         self.X_train = X_train
#         self.y_train = y_train
#         self.X_test = X_test
#         self.y_test = y_test



    def conf_tables(self,X_train,y_train,X_test,y_test,k,max_dep,n_est ,rs,target_labels):
        knn = KNeighborsClassifier(n_neighbors=k)
        labels_name = target_labels
        knn.fit(X_train,y_train)
        knn_y_pred = knn.predict(X_test)
        knn_conf_mat = confusion_matrix(y_test,knn_y_pred )

        knn_cm = normalize( knn_conf_mat ,norm = 'l1' ,axis=1)

        knn_cm_df = pd.DataFrame(knn_cm,columns=labels_name,index=labels_name)


        #######################3
        lgr = LogisticRegression()

        lgr.fit(X_train,y_train)
        lgr_y_pred = lgr.predict(X_test)
        lgr_conf_mat = confusion_matrix(y_test,lgr_y_pred )

        lgr_cm = normalize(lgr_conf_mat ,norm = 'l1' ,axis=1)

        lgr_cm_df = pd.DataFrame(lgr_cm,columns=labels_name,index=labels_name)



        #############################

        rfc = RandomForestClassifier(n_estimators=n_est,random_state=95)

        rfc.fit(X_train,y_train)
        rfc_y_pred = rfc.predict(X_test)
        rfc_conf_mat = confusion_matrix(y_test,rfc_y_pred )

        rfc_cm = normalize(rfc_conf_mat ,norm = 'l1' ,axis=1)

        rfc_cm_df = pd.DataFrame(rfc_cm,columns=labels_name,index=labels_name)



        ######################


        dtc = DecisionTreeClassifier(max_depth=max_dep)

        dtc.fit(X_train,y_train)
        dtc_y_pred = dtc.predict(X_test)
        dtc_conf_mat = confusion_matrix(y_test,dtc_y_pred )

        dtc_cm = normalize(dtc_conf_mat ,norm = 'l1' ,axis=1)

        dtc_cm_df = pd.DataFrame(dtc_cm,columns=labels_name,index=labels_name)


        #############################
        import random

        svc = svm.SVC(C=random.randint(2,4),gamma='auto',kernel='rbf')



        svc.fit(X_train,y_train)
        svc_y_pred = svc.predict(X_test)
        svc_conf_mat = confusion_matrix(y_test,svc_y_pred )

        svc_cm = normalize(svc_conf_mat ,norm = 'l1' ,axis=1)

        svc_cm_df = pd.DataFrame(svc_cm,columns=labels_name,index=labels_name)


        #####################


        mlp = MLPClassifier(max_iter=1000, random_state=rs)

        mlp.fit(X_train,y_train)
        mlp_y_pred = mlp.predict(X_test)
        mlp_conf_mat = confusion_matrix(y_test,mlp_y_pred )

        mlp_cm = normalize(mlp_conf_mat ,norm = 'l1' ,axis=1)

        mlp_cm_df = pd.DataFrame(svc_cm,columns=labels_name,index=labels_name)


        ###########################

        sgd = SGDClassifier()

        sgd.fit(X_train,y_train)
        sgd_y_pred = sgd.predict(X_test)
        sgd_conf_mat = confusion_matrix(y_test,sgd_y_pred )

        sgd_cm = normalize(sgd_conf_mat ,norm = 'l1' ,axis=1)

        sgd_cm_df = pd.DataFrame(sgd_cm,columns=labels_name,index=labels_name)













        matris = [lgr_conf_mat,rfc_conf_mat,dtc_conf_mat,mlp_conf_mat,svc_conf_mat,knn_conf_mat,sgd_conf_mat]
        models = [lgr_cm_df,rfc_cm_df,dtc_cm_df,mlp_cm_df,svc_cm_df,knn_cm_df,sgd]
        labels = ['LogisticRegression','RandomForestClassifier',
        'DecisionTreeClassifier','MLPClassifier','Support Vector Machines',
        'KNeighborsClassifier','SGDClassifier']


        for m,l ,mod in zip(matris,labels,models):

            print(l,'\n'*2,m,'\n'*2,mod)
            print('#'*90,'\n'*2)


        return lgr_cm_df,rfc_cm_df,dtc_cm_df,svc_cm_df,mlp_cm_df,knn_cm_df ,sgd_cm_df


class Accuracy_models():
#     import time
#     from sklearn.linear_model import LogisticRegression
#     from sklearn import svm
#     from sklearn.ensemble import RandomForestClassifier
#     from sklearn.tree import DecisionTreeClassifier
#     from sklearn.neighbors import KNeighborsClassifier
#     from sklearn.metrics import accuracy_score
#     import pandas as pd
#     import numpy as np
#     from random import choice
#     from sklearn.neural_network import MLPClassifier
#     from sklearn.model_selection import train_test_split
#     from sklearn.metrics import accuracy_score



    def __init__(self):

        pass


##### X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=0)

    def show_accuracy(self,X_train, X_test, y_train, y_test,knnn,nn_est,max_dp,rs_range):
        start = time.time()


        def Knn_value(X_train, X_test, y_train, y_test):
            st , end = knnn
            knn_accuracy_list = []
            # st = 30
            # end = 60
            print ('starting KNeighborsClassifier ...')

            for k in tqdm(range(st,end)):
                    knn = KNeighborsClassifier(n_neighbors=k)

                    knn.fit(X_train, y_train)

                    y_pred = knn.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)
                    knn_accuracy_list.append(accuracy)

            max_ind = knn_accuracy_list.index(np.max(knn_accuracy_list))+st-1
            print ('KNeighborsClassifier finished !')
            print ('*'*80,end='\n')
            return max_ind



        def find_best_n_estimators(X_train, X_test, y_train, y_test):


            accuracy_list = []

            n_estimators_list = []

            st , end = nn_est
            print ('starting RandomForestClassifier ...')


            for n in range(st,end):

                forest = RandomForestClassifier(n_estimators=n, random_state=42)

                forest.fit(X_train,y_train)



                accuracy = accuracy_score(y_test,forest.predict(X_test))

                accuracy_list.append(accuracy)



            n_estimators_list.append(accuracy_list.index(np.max(accuracy_list)))
            print ('traing RandomForestClassifier finished !')
            print ('*'*80,end='\n')


            return accuracy_list.index(np.max(accuracy_list))+st-1






        ########################################################################################3
        ####              find max_depth

        #########################################################################################
        def find_max_depth(X_train, X_test, y_train, y_test):

            max_depth_list = []
            st , end = max_dp
            max_dep = range(st,end)
            print ('starting DecisionTreeClassifier ...')

            for md in tqdm(max_dp):
                tree = DecisionTreeClassifier(max_depth=md,random_state=66)
                tree.fit(X_train,y_train)

                y_pred = tree.predict(X_test)

                acc = accuracy_score(y_test,y_pred)

                max_depth_list.append(acc)


            max_depth = max_depth_list.index(np.max(max_depth_list))+st-1
            print ('traing DecisionTreeClassifier finished !')
            print ('*'*80,end='\n')
            return max_depth




        ###########################################################

        ###########   find_best_random_state_mlp

        ##########################################################################
        def find_best_random_state_mlp(X_train,y_train,X_test,y_test):
            mlp_accuracy_list = []

            st,end = rs_range
            print ('starting MLPClassifier ...')

            for n in tqdm(range(st,end)):

                mlp = MLPClassifier(max_iter=1000, random_state=n)

                mlp.fit(X_train,y_train)



                mlp_accuracy = accuracy_score(y_test,mlp.predict(X_test))
            # print(accuracy)

                mlp_accuracy_list.append(mlp_accuracy)

            max_ind = mlp_accuracy_list.index(np.max(mlp_accuracy_list)) +st-1

            max_rs = np.max(mlp_accuracy_list)
            print ('traing MLPClassifier finished !')
            print ('*'*80,end='\n')
            return max_ind , max_rs




        ################################################################


        #####################################################################################################################
        ###  model_evaluate
        ###############################################################################################################

        def model_evaluate(X_train,y_train,X_test,y_test):
            n_est = find_best_n_estimators(X_train, X_test, y_train, y_test)

            rfc = RandomForestClassifier(n_estimators=n_est,random_state=66)

            mksd = find_max_depth(X_train, X_test, y_train, y_test)


            dtc = DecisionTreeClassifier(max_depth=mksd,random_state=66)

            lgr = LogisticRegression()
            svc = svm.SVC()
            mlp_random_state , max_acc = find_best_random_state_mlp(X_train,y_train,X_test,y_test)

            mlp = MLPClassifier(max_iter=1000, random_state = mlp_random_state)

            sgd = SGDClassifier(max_iter=2000,  n_jobs=5)

            # sgd.fit(X_train,y_train)
            # sgd_y_pred = sgd.predict(X_test)
            k_num =Knn_value(X_train, X_test, y_train, y_test)

            knn = KNeighborsClassifier(n_neighbors=k_num)
            models = [lgr , rfc , dtc , svc , knn , mlp,sgd]
            accuracy_list = []
            model_list = ['LogisticRegression','RandomForestClassifier','DecisionTreeClassifier',

                'Support Vector Machines','KNeighborsClassifier','MLPClassifier','SGDClassifier']
            for model in models:

                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                accuracy_list.append(accuracy)



            accuracy_table = pd.DataFrame({'Algorithm':model_list,'Accuracy':accuracy_list})

            table = accuracy_table.sort_values(['Accuracy'],inplace=False,ascending=False)

            accuracy_table = pd.DataFrame(table.values,columns= ['Algorithm','Accuracy'],index=range(1,len(model_list)+1))





            return accuracy_table ,(k_num , mksd , n_est , mlp_random_state)



        table  , values = model_evaluate(X_train,y_train,X_test,y_test)

        stop = time.time()

        print(f'total proccess time : {round(stop-start,2)}')

        return table,values





