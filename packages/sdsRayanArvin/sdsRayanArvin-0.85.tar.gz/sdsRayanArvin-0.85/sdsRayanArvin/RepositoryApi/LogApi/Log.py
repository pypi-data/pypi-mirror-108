from sdsRayanArvin.Repository import Repository


class Log(Repository):
    def SendLog(self, ID_workflows, value, ID_org, typeLog):
        res = self.Request.sendWithOutToken('POST', 'gelf', {
            "type": typeLog,
            "org": ID_org,
            "short_message": ID_workflows,
            "value": value,
        }, 'json')

        return res
