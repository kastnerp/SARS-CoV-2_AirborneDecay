import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class SarsCov2():

    def __init__(self, uv_index, temp, rh, printout=False):

        error_msg = "Not defined for those inputs."

        if uv_index > 10 or uv_index < 0:
            raise ValueError(error_msg)
        elif temp > 30 or temp < 10:
            raise ValueError(error_msg)
        elif rh > 70 or rh < 20:
            raise ValueError(error_msg)

        self.half_life_params = self.HalfLifeParams()

        self.uv_index = uv_index
        self.temp = temp
        self.rh = rh

        decay_50, decay_90, decay_99 = self.calc_covid_half_life(printout)

        self.decay_50 = decay_50
        self.decay_90 = decay_90
        self.decay_99 = decay_99

    def calc_covid_half_life(self, printout):

        solar = (self.uv_index + self.half_life_params.solar_const) / self.half_life_params.solar_scaler
        temp_rc = (self.temp - self.half_life_params.temp_rc_const) / self.half_life_params.temp_rc_scaler
        rh_rc = (self.rh - self.half_life_params.rh_rc_const) / self.half_life_params.rh_rc_scaler
        solar_rc = (solar - self.half_life_params.solar_rc_const) / self.half_life_params.solar_rc_scaler
        intercept_factor = self.half_life_params.intercept
        temp_factor = self.half_life_params.temp_coef * temp_rc
        rh_factor = self.half_life_params.rh_coef * rh_rc
        solar_factor = self.half_life_params.solar_coef * solar_rc
        temp_rh_factor = self.half_life_params.temp_rh_coef * temp_rc * rh_rc
        temp_solar_factor = self.half_life_params.temp_solar_coef * temp_rc * solar_rc
        rh_solar_factor = self.half_life_params.rh_solar_coef * rh_rc * solar_rc
        temp_rh_solar_factor = self.half_life_params.temp_rh_solar_coef * temp_rc * rh_rc * solar_rc
        k_min_denom = intercept_factor + temp_factor + rh_factor + solar_factor + temp_rh_factor + temp_solar_factor + rh_solar_factor + temp_rh_solar_factor

        decay_50_minutes = self.half_life_params.convert_to_time_numerator / k_min_denom

        # decay_50_minutes_hours = decay_50_minutes / 60

        decay90_minutes = (decay_50_minutes * math.log((1 - .90), .5))

        # covid_90_hours = decay90_minutes / 60

        decay_99_minutes = (decay_50_minutes * math.log((1 - .99), .5))

        # covid_99_hours = decay_99_minutes / 60

        if printout is True:

            print("Half-life is: {} min.".format(round(decay_50_minutes, 2)))
            print("90 % decay takes: {} min.".format(round(decay90_minutes, 2)))
            print("99 % decay takes: {} min.".format(round(decay_50_minutes, 2)))

            if decay_50_minutes <= 0:
                print("No decay.")

        return decay_50_minutes, decay90_minutes, decay_99_minutes

    class HalfLifeParams:
        def __init__(self):
            self.solar_const = 0.000281
            self.solar_scaler = 5.4

            self.temp_rc_const = 20.54
            self.temp_rc_scaler = 10.66
            self.rh_rc_const = 45.235
            self.rh_rc_scaler = 28.665
            self.solar_rc_const = 50
            self.solar_rc_scaler = 50

            self.intercept = -7.679348
            self.temp_coef = -1.338432
            self.rh_coef = -0.017835
            self.solar_coef = -7.666331
            self.temp_solar_coef = -1.323633
            self.temp_rh_coef = 0
            self.rh_solar_coef = 0
            self.temp_rh_solar_coef = 0

            self.convert_to_time_numerator = -0.693


temp = 20  # 10...30
rh = 50  # 20...70
uv_index = 5  # 0...10



arr_temp = np.arange(10, 30, 0.2)
arr_uv_index = np.ones(arr_temp.size) * 5
arr_rh = np.ones(arr_temp.size) * 60

arr_sars_cov_2_50 = np.zeros(arr_temp.size)
arr_sars_cov_2_90 = np.zeros(arr_temp.size)
arr_sars_cov_2_99 = np.zeros(arr_temp.size)

for i in range(arr_sars_cov_2_50.size):
    val = SarsCov2(arr_uv_index[i], arr_temp[i], arr_rh[i])
    fifty = val.decay_50
    ninty = val.decay_90
    nintynine = val.decay_99


    arr_sars_cov_2_50[i] = fifty
    arr_sars_cov_2_90[i] = ninty
    arr_sars_cov_2_99[i] = nintynine

#fig, ax = plt.subplots()
ax = sns.scatterplot(y = arr_sars_cov_2_50,x = arr_temp,  label = "Half-life" )
sns.scatterplot(y = arr_sars_cov_2_90,x = arr_temp ,label =  "90 % decay")
sns.scatterplot(y = arr_sars_cov_2_99,x = arr_temp , label =  "99 % decay")
ax.set(xlabel="Temperature [°C]", ylabel="Time to decay [min]")
plt.show()