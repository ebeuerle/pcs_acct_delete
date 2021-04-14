import lib
import csv


class RemoveAccounts():
    def __init__(self):
        self.config = lib.ConfigHelper()
        self.rl_sess = lib.RLSession(self.config.rl_user, self.config.rl_pass, self.config.rl_cust,
                                     self.config.rl_api_base)

    def read_csv_file(self):
        filename = self.config.rl_filename ###<==Configure filename in configs.yml
        acct_id = []
        with open(filename,'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                acct_id.append(row["Id"])

        return acct_id

    def pull_cloud_accounts(self):
        self.url = "https://" + self.config.rl_api_base + "/cloud/name"
        self.rl_sess.authenticate_client()
        allaccts = self.rl_sess.client.get(self.url)

        return allaccts.json()

    def delete_account(self, account_id, all_accts):
        for acct in all_accts:
            if acct['id'] == account_id:
                self.url = "https://" + self.config.rl_api_base + "cloud/" + acct['cloudType'] + "/" + acct['id']
                result = self.rl_sess.client.delete(self.url)
                if result != "200":
                    print("Account id: {} returned error: {}".format(acct['id'],result.status_code))


    def run(self):
        acct_id = self.read_csv_file()
        all_accts = self.pull_cloud_accounts()
        for acct in acct_id:
            self.delete_account(acct,all_accts)

def main():
    Remove_Accounts = RemoveAccounts()
    Remove_Accounts.run()

if __name__ == "__main__":
    main()