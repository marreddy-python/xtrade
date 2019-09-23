from flask import Blueprint, request,render_template,redirect, url_for,session,logging,flash,session,json,jsonify,flash
import sys
sys.dont_write_bytecode = True

from myapp.controllers.interface import StrategyController,Strategy,DataController
from myapp.controllers.decides_start_end import myFunction
from myapp.controllers.add_favourite import addFav,deletestrategy
from myapp.controllers.check_strategyapplied import applied_or_not,strategy_savedornot

modulo1_blueprint = Blueprint(name='modulo1', import_name=__name__,template_folder='templates',
static_folder='static', static_url_path='/login,/trades.svg,/infile.json')


from myapp.models.users import Post
import time

#LOGIN PAGE
@modulo1_blueprint.route('/', methods=['GET','POST'])
@modulo1_blueprint.route('/login', methods=['GET','POST'])
def login():
       
        if request.method == "POST":

                uname = request.form["uname"]
                passw = request.form["passw"]
        
                login = Post.query.filter_by(username=uname, password=passw).first()

                if login is not None:
                        print uname 
                        flash('Logged in successfully.')
                        return redirect(url_for("modulo1.strategyview"))
            
        
        return render_template("login.html")


#REGISTRATION PAGE
@modulo1_blueprint.route('/register', methods=['GET','POST'])
def register():

        if request.method == "POST":
                uname = request.form['uname']
                mail = request.form['mail']
                passw = request.form['passw']
                register = Post(username = uname, email = mail, password = passw)
                db.session.add(register)
                db.session.commit()
       
                return redirect(url_for("modulo1.login"))
                
        return render_template("register.html")



@modulo1_blueprint.route('/logout', methods=['GET','POST'])
def logout():
    return redirect(url_for('modulo1.login'))



start_time = None 
end_time = None
St = None
Trades_singleday = None
Metric_values_singleday = None
Performance = None
Buy_flags = None
Sell_flags = None
Stratey_values = None


@modulo1_blueprint.route('/strategyview', methods=['GET','POST'])
def strategyview():

        global start_time,end_time,St, Performance,Metric_values_singleday,Trades_singleday,Buy_flags,Sell_flags,Stratey_values

        Data_loader = DataController()
       
        # end_time = int(round(time.time() * 1000))
        
        #MYFUNCTION WILL DECIDE THE START TIME AND END TIME FOR THE CHART 
        start_time,end_time = myFunction()
       
        print start_time,end_time

        # daily_data = Data_loader.MarketData(start_time,end_time)
        tweenty_days = end_time - (86400000*20)
        # daily_data = Data_loader.MarketData(start_time,end_time)
        daily_data = Data_loader.MarketData(tweenty_days,start_time)
        # print daily_data


        if request.method == "POST":  

                Buying_angle = int(request.form.get('Buying_angle')) 
                selling_angle = int(request.form.get('selling_angle'))
                optimization = str(request.form.get('Optimization'))
                relative_angle = int(request.form.get('relative_angle'))
                stop_order = str(request.form.get('STPODVALUE'))
                less_than_buy = float(request.form.get('less_than_buy'))
                
                print(Buying_angle,selling_angle,optimization,relative_angle,stop_order,less_than_buy)
                
                Stratey_values = [Buying_angle,selling_angle,optimization,relative_angle,stop_order,less_than_buy] 

                if selling_angle == '' and Buying_angle == '':
                        print '--------------------------------FAILED-----------------------------'
                        # FLASH MESSAGE NEEDS TO BE HERE 
                        return jsonify({'Trades_singleday':0,'Metric_values': 0 })
                
                else:
                        # INSTANCE OF STRATEGY CLASS
                        St = Strategy(1,Stratey_values,'NONE')
                        # data_st.man  = St

                        # STRATEGY CONTROLLER 
                        startegy_loader = StrategyController()

                        #After clicking on apply button
                        if request.form.get('main') == 'Apply': 

                                # strategy should be applied for 20days 
                                tweenty_days = end_time - (86400000*20)
                                startegy_loader.applyStrategy('TVIX',St ,start_time,tweenty_days) 
                                # Getting the trades and metric values for a single day
                                Trades_singleday,Buy_flags,Sell_flags = Data_loader.getTrades('TVIX',St,start_time,tweenty_days)
                                Metric_values_singleday = Data_loader.getPerformance('TVIX',St,start_time,end_time)
                                Performance = Data_loader.getPerformance('TVIX',St ,start_time,tweenty_days)
                                
                                # return both trades and metric values 
                                return jsonify({'Trades_singleday':Trades_singleday,'Metric_values': Metric_values_singleday,'Performance':Performance,'Buy_flags':Buy_flags,'Sell_flags':Sell_flags , })

                        #After Clicking on save button
                        if request.form.get('main') == 'Save':
                                # Check if strategy is already applied or not, if not applied apply, if applied save strategy
                                tweenty_days = end_time - (86400000*20)
                                sus = applied_or_not(St,start_time,tweenty_days)
                                print sus

                                if sus ==  'notexist':
                                        # Check if strategy is already applied or not if not applied apply, if applied save strategy
                                        tweenty_days = end_time - (86400000*20)
                                        b = startegy_loader.applyStrategy('TVIX',St ,start_time,tweenty_days)
                                        Trades_singleday,Buy_flags,Sell_flags = Data_loader.getTrades('TVIX',St,start_time,tweenty_days)
                                        Metric_values_singleday = Data_loader.getPerformance('TVIX',St,start_time,end_time)
                                        b = startegy_loader.saveStrategy(St,start_time,tweenty_days)
                                        Performance = Data_loader.getPerformance('TVIX',St ,start_time,tweenty_days)
                                       
                                        return jsonify({'Trades_singleday':Trades_singleday,'Metric_values': Metric_values_singleday,'Performance':Performance,'Buy_flags':Buy_flags,'Sell_flags':Sell_flags  })
                                
                                else:
                                        ma = strategy_savedornot(St,start_time,tweenty_days)
                                        if ma == 'notsaved':
                                                b = startegy_loader.saveStrategy(St,start_time,tweenty_days)
                                                return json.dumps({'status':'Strategy_saved'})
                                        else:
                                                return json.dumps({'status':'Strategy_alredy_saved'})


                        #After clicking on save_and_compare button
                        elif request.form.get('main') == 'Save_and_compare':


                                tweenty_days = start_time - (86400000*20)
                                b = startegy_loader.applyStrategy('TVIX',St ,start_time,tweenty_days)
                                
                                Trades_singleday,Buy_flags,Sell_flags = Data_loader.getTrades('TVIX',St,start_time,end_time)
                                Metric_values_singleday = Data_loader.getPerformance('TVIX',St,start_time,end_time)
                                b = startegy_loader.saveStrategy(St,start_time,tweenty_days)
                                Performance = Data_loader.getPerformance('TVIX',St ,start_time,tweenty_days)

                                return jsonify({'Trades_singleday':Trades_singleday,'Metric_values': Metric_values_singleday,'Performance':Performance })

                                
                        else:
                                return json.dumps({'status':'Failed'})

       
        else:
                
                Data_loader = DataController()
                data,strategy_names = Data_loader.getStrategies()
                print 'data',data 
                print 'Stratey_values',Stratey_values
                return render_template("page1.html", Metric_values_singleday = Metric_values_singleday,Trades_singleday = Trades_singleday,Performance = Performance,daily_data = daily_data,Buy_flags = Buy_flags,Sell_flags = Sell_flags,
                strategy_names = strategy_names,Strategy_values =Stratey_values)



@modulo1_blueprint.route('/Arena', methods=['GET','POST'])
def Arena():  
        Data_loader = DataController()
        data,strategy_names = Data_loader.getStrategies()
        return render_template("page2.html",strategy_names = strategy_names, )     

         

@modulo1_blueprint.route('/Strategies1', methods=['GET','POST'])
def Strategies1():

        if request.method == "POST": 

                # GET THE ID OF A CLICKED STARTEGY AND ADD TO FAVOURITES
                print 'EXCELLENT '
                print (request.get_data())
                # adding strategy to favouites
                addFav(request.get_data())
                
                # get the updated strategies 
                Data_loader = DataController()
                data123,strategy_names = Data_loader.getStrategies()
                print data123
                return data123
                
        else:
                #HERE LOAD ALL THE STRATEGIES FROM THE STRATEGIES TABLE

                Data_loader = DataController()
                data,strategy_names = Data_loader.getStrategies()
                print strategy_names,data

                return render_template("page3.html", data = data ,strategy_names = strategy_names )



@modulo1_blueprint.route('/settings', methods=['GET','POST'])
def settings():
    
        if request.method == "POST":

                price_history = request.form.get('Price_history')
                data_grouping_Interval = request.form.get('data_grouping_Interval')
                userinput_dg = request.form.get('userinput_dg')
                userinput_sma = request.form.get('userinput_sma')
                position_size = request.form.get('Position_size')
                arena_size = request.form.get('max_size_arena')

                print (price_history,data_grouping_Interval,userinput_dg,userinput_sma,position_size,arena_size)

                #Save Button
                if request.form.get('main') == 'Save':
                        return json.dumps({'status':'Save'})

                #Cancel button
                if request.form.get('main') == 'Cancel':
                        return json.dumps({'status':'Cancel'})

        else:   
                # HERE LOAD THE SETTINGS FROM THE DATABASE AND PASS IT TO PAGE4 TEMPLATE
                Data_loader = DataController()
                data,strategy_names = Data_loader.getStrategies()
                
                return render_template("page4.html",strategy_names = strategy_names,)
         




@modulo1_blueprint.route('/delete_strategy', methods=['GET','POST'])
def delete_strategy():
        if request.method == "POST":
                
        

                print request.form.get('clicked_strategy')

                deletestrategy(request.form.get('clicked_strategy'))

                return json.dumps({'status':'Deleted ssuccesfully'})


