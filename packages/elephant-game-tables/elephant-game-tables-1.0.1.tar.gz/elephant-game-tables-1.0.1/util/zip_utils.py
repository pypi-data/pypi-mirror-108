import gzip


class ZipUtils:
    @staticmethod
    def create_zip_file(output_path, files):
        try:
            gz = gzip.GzipFile(output_path, 'wb')
            for file_name, file_content in files.items():
                if file_content:
                    gz.write(file_content.encode('utf-8'))
            gz.close()
            return True
        except Exception as e:
            print("create zip file error!", output_path, files, e)
            return False
