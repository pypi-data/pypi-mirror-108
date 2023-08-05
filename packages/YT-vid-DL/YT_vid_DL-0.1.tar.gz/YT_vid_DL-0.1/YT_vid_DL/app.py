import YT_downloader

url = input("Enter the link: ")

yt = YT_downloader.AgeRestrictedYTVideo(url)

age_restricted = yt.is_age_restricted()

if age_restricted:
    bytes_obj = yt.get_video()
    print(f'Byte object returned for {url} with size {bytes_obj.getbuffer().nbytes} bytes')
