import pandas as pd 

def main():
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


if __name__ == "__main__":
    main()