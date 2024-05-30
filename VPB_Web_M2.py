import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import minimize

st.title('Product Package Optimal Pricing')

st.subheader("Customer's Requirements")
st.write("Write customer's overall requirements for products here. In case competitor is offering lower interest rate/fee." 
         "Please indicate this amount as interest rate input. ")

# ///////////

# cus_info_table = pd.read_excel(r'D:\VPB Hackathon\SampleData2\Model2_input_data.xlsx').set_index('CusID')
cus_info_table = pd.read_excel('https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fyenlh8%2FVPB_Hackathon%2Fmain%2FModel2_input_data.xlsx&wdOrigin=BROWSELINK', engine='openpyxl').set_index('CusID')

CusID1, CusName, empty_col = st.columns(3)
CusID = CusID1.number_input('CusID', value = None, min_value = 9000, max_value = 9999, format = '%d')
if CusID == None:
    CusName = None
elif CusID not in cus_info_table.index:
    
    st.markdown(''':red[Customer not found.Please enter CusID again!] ''')
else:
    CusName = cus_info_table.loc[CusID, 'CusName']
    st.write('Customer Name:', CusName)

# ///////////////

options = st.multiselect(
    "Information on Product Constraints",
    ["Short Term Loan", "Term Deposit", "CASA"], default = None)
st.write('')
st.write('')

# st.write(options)
# def form_creation():
st.write('Fill constraints in table below. Leave the cell blank if there is no constrained requirement.')
prods = []
for i in range(len(options)):
    prods.append(options[i])

with st.form('Constraints/Requirements Input'):

    RM_input = pd.DataFrame([], columns = ['Product', 'Amount (VNDm)', 'Term (Month)', 'Interest Rate'])
    for i in range(len(prods)):
        RM_input.loc[i, 'Product'] = prods[i]
        
    RM_input.set_index('Product', inplace = True)
    if len(prods)>0:
        edited_RM_input = st.data_editor(RM_input, disabled = ('Product'))
    else:
        st.write('')
    
    submitted = st.form_submit_button('Confirm Information')



# /////////////////////////



# ///////////////////////////////

# TD_Rate_Standard = pd.read_excel(r'D:\VPB Hackathon\SampleData2\TD_Rate_Standard.xlsx').set_index('Months_Num')
TD_Rate_Standard = pd.read_excel('https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fyenlh8%2FVPB_Hackathon%2Fmain%2FTD_Rate_Standard.xlsx&wdOrigin=BROWSELINK', engine='openpyxl').set_index('Months_Num')


# calc_button = st.button('Click me!')

if submitted:
    st.subheader("Proposed Product Package Pricing")
    # st.write(edited_RM_input.loc['Short Term Loan', 'Term (Month)'])
    # Set boundaries for variables:

    # if 'CASA' in prods and RM_input.loc['CASA', 'Amount (VNDm)'] !=None:
    #     CASA_amount_bound = (cus_info_table.loc[CusID, 'CASA_Amount_Min'], max(cus_info_table.loc[CusID, 'CASA_Amount_Max'], RM_input.loc['CASA', 'Amount (VNDm)']))
    # else:
    #     CASA_amount_bound = (cus_info_table.loc[CusID, 'CASA_Amount_Min'], cus_info_table.loc[CusID, 'CASA_Amount_Max'])
    CASA_amount_bound = (cus_info_table.loc[CusID, 'CASA_Amount_Min'], cus_info_table.loc[CusID, 'CASA_Amount_Max'])
    CASA_term_bound = (1, 12)

    # if 'Term Deposit' in prods and RM_input.loc['Term Deposit', 'Amount (VNDm)'] != None:
    #     TD_amount_bound = (cus_info_table.loc[CusID, 'TD_Amount_Min'], max(cus_info_table.loc[CusID, 'TD_Amount_Max'], RM_input.loc['Term Deposit', 'Amount (VNDm)']))
    # else:
    #     TD_amount_bound = (cus_info_table.loc[CusID, 'TD_Amount_Min'], cus_info_table.loc[CusID, 'TD_Amount_Max'])
    TD_amount_bound = (cus_info_table.loc[CusID, 'TD_Amount_Min'], cus_info_table.loc[CusID, 'TD_Amount_Max'])

    TD_CI_bound = (cus_info_table.loc[CusID, 'TD_FTP'], 0.15)
    TD_term_bound = (1, 12)

    if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Interest Rate'] != None:
        ST_CI_bound = (cus_info_table.loc[CusID, 'STL_CI_Min'], float(edited_RM_input.loc['Short Term Loan', 'Interest Rate']))
    else:
        ST_CI_bound = (cus_info_table.loc[CusID, 'STL_CI_Min'], cus_info_table.loc[CusID, 'STL_CI_Max'])

    
    if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'] != None:
        ST_amount_bound = (float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)']), float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)']))
    else:
        ST_amount_bound = (cus_info_table.loc[CusID, 'STL_Amount_Min'], cus_info_table.loc[CusID, 'STL_Amount_Max'])


    if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Term (Month)'] != None:
        ST_term_bound = (float(edited_RM_input.loc['Short Term Loan', 'Term (Month)']),float(edited_RM_input.loc['Short Term Loan', 'Term (Month)'])) 
    else:
        ST_term_bound =(1,12) #Short term loan period
    # ST_amount_inputed = RM_input.loc['Shor Term Loan', 'Amount (VNDm)']
    # ST_amount_bound = (cus_info_table.loc[CusID, 'STL_Amount_Min'], ST_amount_inputed)

    # ST_term_bound = RM_input.loc['Short Term Loan', 'Term (Month)']

    # bounds = [CASA_amount_bound, CASA_term_bound, TD_amount_bound, TD_CI_bound, TD_term_bound, ST_CI_bound, ST_amount_bound, ST_term_bound]
    # bounds = [CASA_amount_bound, CASA_term_bound, TD_amount_bound, TD_CI_bound, TD_term_bound, ST_CI_bound, ST_amount_bound]
    bounds = [CASA_amount_bound, CASA_term_bound, TD_amount_bound, TD_CI_bound, TD_term_bound, ST_CI_bound, ST_amount_bound, ST_term_bound]

    # Define Objective:
    def objective_func(x):
        if 'CASA' in prods and edited_RM_input.loc['CASA', 'Amount (VNDm)'] != None:
            x1 = float(edited_RM_input.loc['CASA', 'Amount (VNDm)'])
        else:
            x1 = x[0] #CASA amount
        if 'CASA' in prods and edited_RM_input.loc['CASA', 'Term (Month)'] != None:
            x2 = float(edited_RM_input.loc['CASA', 'Term (Month)'])
        else:
            x2 = x[1] # CASA term
        if 'Term Deposit' in prods and edited_RM_input.loc['Term Deposit', 'Amount (VNDm)'] != None:
            x3 = float(edited_RM_input.loc['Term Deposit', 'Amount (VNDm)'])
        else:
            x3 = x[2] #TD amount
        
        x4 = x[3] #TD CI
        
        if 'Term Deposit' in prods and edited_RM_input.loc['Term Deposit', 'Term (Month)'] != None:
            x5 = float(edited_RM_input.loc['Term Deposit', 'Term (Month)'])
        else:
            x5 = x[4] #TD term
        
    
        x6 = x[5] #Short term loan CI
        
        if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'] != None:
            x7 = float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'])
        else:
            x7 = x[6] #Short term loan amount

        if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Term (Month)'] != None:
            x8 = float(edited_RM_input.loc['Short Term Loan', 'Term (Month)'])
        else:
            x8 = x[7] #Short term loan period

        # return -((x1*(cus_info_table.loc[CusID, 'CASA_FTP'] - cus_info_table.loc[CusID, 'CASA_CI'])*x2/12)
        #         +(x3*(cus_info_table.loc[CusID, 'TD_FTP']-x4)*x5/52)
        #         + (x7*(x6-cus_info_table.loc[CusID, 'STL_FTP']-cus_info_table.loc[CusID, 'EL'])*x8/12)-cus_info_table.loc[CusID, 'CASA_serve_cost']*x1-cus_info_table.loc[CusID, 'TD_serve_cost']*x3-cus_info_table.loc[CusID, 'STL_serve_cost']*x7) 

  
        # x1 = x[0]
        # x2 = x[1]
        # x3 = x[2]
        # x4 = x[3]
        # x5 = x[4]
        # x6 = x[5]
        # x7 = x[6]
        # x7 = RM_input.loc['Short Term Loan', 'Amount (VNDm)']
        
        # x8 = x[7]
        
        # x8 = RM_input.loc['Short Term Loan', 'Term (Month)']

        # return -((x1*(cus_info_table.loc[CusID, 'CASA_FTP'] - cus_info_table.loc[CusID, 'CASA_CI'])*x2/12)
        #         +(x3*(cus_info_table.loc[CusID, 'TD_FTP']-x4)*x5/52)
        #         + (float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'])*(x6-cus_info_table.loc[CusID, 'STL_FTP']-cus_info_table.loc[CusID, 'EL'])*float(edited_RM_input.loc['Short Term Loan', 'Term (Month)'])/12)
        #         -cus_info_table.loc[CusID, 'CASA_serve_cost']*x1
        #         -cus_info_table.loc[CusID, 'TD_serve_cost']*x3
        #         -cus_info_table.loc[CusID, 'STL_serve_cost']*float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)']))

        return -((x1*(cus_info_table.loc[CusID, 'CASA_FTP'] - cus_info_table.loc[CusID, 'CASA_CI'])*x2/12)
                +(x3*(cus_info_table.loc[CusID, 'TD_FTP']-x4)*x5/52)
                + (x7*(x6-cus_info_table.loc[CusID, 'STL_FTP']-cus_info_table.loc[CusID, 'EL'])*x8/12)
                -cus_info_table.loc[CusID, 'CASA_serve_cost']*x1
                -cus_info_table.loc[CusID, 'TD_serve_cost']*x3
                -cus_info_table.loc[CusID, 'STL_serve_cost']*x7)


    # Define constraints:
    ### Short term Loan Customer Interest Rate cannot exceed RM input:
    
    # def inequality_constraint_ST_CI(x):
    #     x6 = x[5]
    #     if len(prods)==0:
        
    #         return min(cus_info_table.loc[CusID, 'STL_CI_Max'], cus_info_table.loc[CusID, 'STL_CI_Competitor']) - x6
           
    #     else if len(prods)>0:
    #         return float(edited_RM_input.loc['Short Term Loan', 'Interest Rate']) - x6
        
        

    ### Term Deposit Rate cannot be smaller than Standard Rate applied for normal customer:
    mylist = [1,2,3,4,5,6,7,8,9,10,11,12]
    def inequality_constraint_TD_CI_standard(x):
        x4 = x[3] #TD CI
        x5 = x[4] #TD Term
        return x4 - TD_Rate_Standard.loc[min(mylist, key=lambda x:abs(x-x5)), 'TD_CI']
    # st.write(TD_Rate_Standard.loc[min(mylist, key=lambda x:abs(x-1)), 'TD_CI'])
    ### Term Deposit Rate cannot be larger than internal regulations, assume 2% above standard rates is the allowable policy:
    def inequality_constraint_TD_CI_policy(x):
        x4 = x[3]
        x5 = x[4]
        return TD_Rate_Standard.loc[min(mylist, key=lambda x:abs(x-x5)), 'TD_CI']+2% - x4

    # constraint1 = {'type': 'ineq', 'fun': inequality_constraint_ST_CI}
    constraint2 = {'type': 'ineq', 'fun': inequality_constraint_TD_CI_standard}
    constraint3 = {'type': 'ineq', 'fun': inequality_constraint_TD_CI_policy}

    # Set initial variable vector values:

    # init_var_object = [cus_info_table.loc[CusID, 'CASA_Amount_Min'], 1, cus_info_table.loc[CusID, 'TD_Amount_Min'], 0.005, 1, 0.05, cus_info_table.loc[CusID, 'STL_Amount_Min'], 1]
    # init_var_object = [cus_info_table.loc[CusID, 'CASA_Amount_Min'], 1, cus_info_table.loc[CusID, 'TD_Amount_Min'], 0.005, 1, RM_input.loc['Short Term Loan', 'Interest Rate']]

    if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'] != None:
        init_ST_Amount = float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'])
    
    else:
        init_ST_Amount =cus_info_table.loc[CusID, 'STL_Amount_Min'] #Short term loan amount

    if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Term (Month)'] != None:
        init_ST_term = float(edited_RM_input.loc['Short Term Loan', 'Term (Month)'])
    else:
        init_ST_term = 12 #Short term loan period



    init_var_object = [cus_info_table.loc[CusID, 'CASA_Amount_Max'], 1, cus_info_table.loc[CusID, 'TD_Amount_Max'], 0.05, 12, float(cus_info_table.loc[CusID, 'STL_CI_Min']), init_ST_Amount, init_ST_term]

    # Run Optimization Model:
    result = minimize(objective_func, init_var_object, constraints = [constraint2, constraint3], method = 'SLSQP', bounds = bounds)

   
    # st.write(result.x[0], result.x[1], result.x[2], result.x[3], result.x[4], result.x[5], result.x[6], result.x[7])

             
    

    # Calculate profits by product:
    CASA_profit = result.x[0]*(cus_info_table.loc[CusID, 'CASA_FTP'] - cus_info_table.loc[CusID, 'CASA_CI'])*result.x[1]/12 - cus_info_table.loc[CusID, 'CASA_serve_cost']*result.x[0]
    TD_profit = result.x[2]*(cus_info_table.loc[CusID, 'TD_FTP']-result.x[3])*result.x[4]/12 - cus_info_table.loc[CusID, 'TD_serve_cost']*result.x[2]
    # ST_profit = float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'])*(result.x[5]-cus_info_table.loc[CusID, 'STL_FTP']-cus_info_table.loc[CusID, 'EL'])*float(edited_RM_input.loc['Short Term Loan', 'Interest Rate'])/12 -cus_info_table.loc[CusID, 'STL_serve_cost']*float(edited_RM_input.loc['Short Term Loan', 'Amount (VNDm)'])
    ST_profit = result.x[6]*(result.x[5]-cus_info_table.loc[CusID, 'STL_FTP']-cus_info_table.loc[CusID, 'EL'])*result.x[7]/12 -cus_info_table.loc[CusID, 'STL_serve_cost']*result.x[6]


               


    # Create result table:
    # [CASA_amount_bound, CASA_term_bound, TD_amount_bound, TD_CI_bound, TD_term_bound, ST_CI_bound, ST_amount_bound, ST_term_bound]

    dic = { 'Product': ['CASA', 'TD', 'ST'], 'Amount (VNDm)': [round(result.x[0],0), round(result.x[2],0), round(result.x[6],0)],
        'Term (Month)': [round(result.x[1],0), round(result.x[4],0), round(result.x[7])],
        'Customer Interest Rate': [cus_info_table.loc[CusID, 'CASA_CI'], result.x[3], result.x[5]], 
        'Profit (VNDm)': [CASA_profit, TD_profit, ST_profit]}

    Result_Table = pd.DataFrame(dic)



    Result_Table.loc['Total', 'Profit (VNDm)'] = Result_Table['Profit (VNDm)'].sum()
    for i in ['Product', 'Amount (VNDm)', 'Term (Month)', 'Customer Interest Rate']:
        Result_Table.loc['Total', i] = ''

    Result_Table.style.format(precision = 0.2)

    # st.markdown(''':violet[Compare Benefits for the Bank] ''')
    
    # if len(prods) == 0:
    # # options == None or ((edited_RM_input['Amount (VNDm)'].values.all() == None) and (edited_RM_input['Term (Month)'].values.all() == None) and (edited_RM_input['Interest Rate'].values.all() == None)):
    #     st.write('')

        
    # else:
        # st.dataframe(Result_Table)
    if 'Short Term Loan' in prods and float(edited_RM_input.loc['Short Term Loan', 'Interest Rate'])>0:
        Competitor_ST_CI = float(edited_RM_input.loc['Short Term Loan', 'Interest Rate'])
    else:
        Competitor_ST_CI = cus_info_table.loc[CusID, 'STL_CI_Competitor'] # Assume competitor information already taken into account by this CI Max

#  if 'Short Term Loan' in prods and edited_RM_input.loc['Short Term Loan', 'Interest Rate'] != None:
#         ST_CI_bound = (cus_info_table.loc[CusID, 'STL_CI_Min'], float(edited_RM_input.loc['Short Term Loan', 'Interest Rate']))
#     else:
#         ST_CI_bound = (cus_info_table.loc[CusID, 'STL_CI_Min'], cus_info_table.loc[CusID, 'STL_CI_Max'])


        # if 'Term Deposit' in prods and float(edited_RM_input.loc['Term Deposit', 'Term (Month)'])>0:
        #     TD_term_result = float(edited_RM_input.loc['Term Deposit', 'Term (Month)'])
        # else:
    TD_term_result = int(round(float(result.x[4]),0)) #TD term

    # st.write(TD_Rate_Standard.loc[min(mylist, key=lambda x:abs(x-TD_term_result)), 'TD_CI'])
    dic_cus = {'Product': ['CASA', 'TD', 'ST'],
                'Customer Interest Rate Proposed': [cus_info_table.loc[CusID, 'CASA_CI'], result.x[3], result.x[5]],
                    'Customer Interest Rate Standard/Competitor':[cus_info_table.loc[CusID, 'CASA_CI'], TD_Rate_Standard.loc[min(mylist, key=lambda x:abs(x-TD_term_result)), 'TD_CI'], Competitor_ST_CI]} 


        # st.markdown(''':violet[Compare Customer Benefits] ''')

    Cus_Compare_Table = pd.DataFrame(dic_cus)
    

    Cus_Compare_Table.style.format(precision=3, thousands=".", decimal=",") \
    # st.dataframe(Cus_Compare_Table)
    st.markdown(''':violet[Compare Benefits for the Bank] ''')
    st.dataframe(Result_Table, column_config = dict(CI = st.column_config.NumberColumn('Customer Interest Rate', format = '%.2f %%'),
                                                   Amount = st.column_config.NumberColumn('Amount (VNDm', format = '%.2f'),
                                                   Term = st.column_config.NumberColumn('Term (Month)', format = '%.f'),
                                                   Profit = st.column_config.NumberColumn('Profit (VNDm', format = '%.2f')
                                                                                      ))

    st.write('')
    st.markdown(''':violet[Compare Customer Benefits] ''')
    st.dataframe(Cus_Compare_Table, column_config = dict(CI_proposed = st.column_config.NumberColumn('Customer Interest Rate Proposed', format = '%.2f %%'),
                                                         competitor = st.column_config.NumberColumn('Customer Interest Rate Standard/Competitor', format = '%.2f %%')))

    st.write('')
    st.button("Reset", type="primary")
    cal_button = False
else:
    None
   
reset_button = st.button('Reset', 'primary')

if reset_button == True:
    calc_button = False
    CusID1 = CusID1.number_input('CusID', value = None, min_value = 9000, max_value = 9999, format = '%d')
    RM_input = pd.DataFrame([], columns = ['Product', 'Amount (VNDm)', 'Term (Month)', 'Interest Rate'])
    edited_RM_input = st.data_editor(RM_input, disabled = ('Product'))
    options = st.multiselect("Information on Product Constraints",
    ["Short Term Loan", "Term Deposit", "CASA"], default = None)
    # editable
    
    # st.write(result)
