from datetime import datetime, timedelta

import pandas as pd
import pytz

import pixela_tracking as pt
import sign_in_up


def main():
    utc_timezone = pytz.timezone("UTC")
    seven_dates = [(datetime.now(utc_timezone).date() - timedelta(i)) for i in range(7)]
    # print(seven_dates)

    all_surahs = (
        pd.read_csv("data/All_Surahs.csv").set_index("Surahs")["Ayahs"].to_dict()
    )

    # v = [key for key in all_surahs]
    # print(type(all_surahs.keys()))
    # print(v)

    current = pd.read_csv("data/current.csv", header=None)
    surah = current[0].values[0]
    verse = current[1].values[0]
    # #print(current)
    # print(surah)
    # print(verse)

    outside = sign_in_up.SignInUp()

    pt.update_history()
    if outside.signed_in:
        inside = pt.Tracking(
            dates=seven_dates,
            all_surah=all_surahs,
            current_surah=surah,
            current_verse=verse,
        )


if __name__ == "__main__":
    main()
