class lists:

    def list_yes(self):
        list = ['yes', 'sure', 'ok', 'definitely',
                'okay', 'yea', 'alright', 'roger', 'aye',
                'indeed', 'affirmative', 'certainly', 'indeed',
                'absolutely']
        return list


    def list_no(self):
        list = ['no', 'negative', 'never',
                'nay', 'not', 'nope']
        return list

    def list_ticker(self):
        from simplelist import listfromtxt
        list = listfromtxt('list.txt')
        return list

