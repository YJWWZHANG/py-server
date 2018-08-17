class Version(object):

    def __init__(self, update, new_version, apk_file_url, update_log, target_size, new_md5, constraint): 
        self.update = update
        self.new_version = new_version
        self.apk_file_url = apk_file_url
        self.update_log = update_log
        self.target_size = target_size
        self.new_md5 = new_md5
        self.constraint = constraint

    def __str__(self):
        return 'Version object (%s, %s, %s, %s, %s, %s, %s)' % (self.update, self.new_version, self.apk_file_url, self.update_log, self.target_size, self.new_md5, self.constraint)
