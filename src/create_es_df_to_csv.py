import pandas as pd 

def awareness_dataset():
    sec_df = pd.read_excel('IT Security Awareness Global report.xlsx')

    sec_df  = sec_df.drop(columns=['Username','FunctionalAreaName','CostCenterName',
                                'Time spent on test','Community name','Content name',
                                'Course specified approver','TradeAssignment(Attribute8)',
                                'SalesOrganizationName','SalesOrganizationCode','FunctionalAreaCode',
                                'FirstName','LastName',"Creator approver","Manager approver","Specified Approver",
                                "Approval date",'Suspend data'])

    sec_df[["Last login", "Last activity","Registration date", "Created","Date course completed"]].apply(
                                            pd.to_datetime,format="%Y-%m-%dT%H:%M:%S",errors='coerce')
                                            
    sec_df["Last login"]=sec_df["Last login"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    sec_df["Last activity"] = sec_df["Last activity"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    sec_df["Registration date"] = sec_df["Registration date"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    sec_df["Date course completed"] = sec_df["Date course completed"].dt.strftime("%Y-%m-%dT%H:%M:%S")


    sec_df.to_csv('hilti.csv',index=False)

def phising_dataset():
    xls = pd.ExcelFile('../DataPhishingReport.xlsx')
    df1 = pd.read_excel(xls,'Attachments')
    df2 = pd.read_excel(xls,'Blank')
    df3 = pd.read_excel(xls,'Spam')
    df4 = pd.read_excel(xls,"RealPhishing")
    df5 = pd.read_excel(xls,"Internal Phishing")

    df1.insert(3,'Filename','Attachments')
    df2.insert(3,'Filename','Blank')
    df3.insert(3,'Filename','Spam')
    df4.insert(3,'Filename','RealPhising')
    df5.insert(3,'Filename','Internal Phising')


    df4 = df4.drop(['Sender','TicketNr','More than 1 recipient'],axis=1)
    df4= df4.reindex(['Subject',"Date",'UserID','Filename'],axis=1)
    df4.columns = ['Subject','Received','Sender','Filename']

    df_list = [df1,df2,df3,df4,df5]

    dataset = pd.concat(df_list)
    dataset = dataset.reset_index()
    dataset['Received'] = pd.to_datetime(dataset['Received'], errors='coerce')
    dataset['Received']=dataset['Received'].dt.strftime("%Y-%m-%dT%H:%M:%S")
    dataset = dataset.drop(['index'],axis=1)
    dataset.to_csv('dataPhising.csv',index=False)

if __name__ == "__main__":
    awareness_dataset()
    phising_dataset()