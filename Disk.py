import os


class Disk:

    @staticmethod
    def current_usage():
        st = os.statvfs('/')
        free = round((st.f_bavail * st.f_frsize / 1024 / 1024), 2)
        total = round((st.f_blocks * st.f_frsize / 1024 / 1024), 2)
        used = round(((st.f_blocks - st.f_bfree) * st.f_frsize) / 1024 / 1024, 2)
        percent = round(used / total * 100, 2)
        return {
            "total": total,
            "used": used,
            "free": free,
            "percent_used": percent
        }

