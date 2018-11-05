"""
MuonTest, a python script for running 500 Monte Carlo Simulations of Muon Lifetime Measurement

Authors: Azid Harun

Date :  05/10/2018

"""
# Import required packages
import numpy as np
from MyMuon import MyMuonX
import pylab as pl
from tqdm import tqdm

def main():

    # Create dict for storing data
    data = {}
    data['estimated tau'] = []

    # Define a Muon class 
    tau_true = 2.2
    Muon = MyMuonX(0.0, 10.0, 1/tau_true)

    # 500 Monte Carlo Simulations for Muon Lifetime Measurement
    for i in tqdm(range(500)):

        data['x'] = []
        data['y-line'] = []

        # Get 1000 muon decay times and their respective pdf points
        for i in MyMuonX(0.0, 10.0, 1/tau_true):
            data['x'].append(i[0])
            data['y-line'].append(i[1])

        # Calculate the estimated lifetime for i-th simulation
        tau_estimate = Muon.integralNumeric(data['x'], False)

        # Store the estimated lifetime for i-th simulation
        data['estimated tau'].append(tau_estimate)

    # Save data
    # np.savetxt('MuonDecayTime.txt', data['x'])

    #Calculate the average estimated lifetime from 500 simulations
    tau_ave = Muon.integralNumeric(data['estimated tau'], False)

    #Get pdf points for true and average estimated lifetime
    f_tau_true = Muon.f(1/tau_true)
    f_tau_ave = MyMuonX(0.0, 10.0, 1/tau_ave).f(1/tau_ave)

	# Calculate the error in the estimated lifetime calculated
    single_error_estimated_tau = np.std(data['estimated tau'])
    error_estimated_tau = np.std(data['estimated tau'])/np.sqrt(len(data['estimated tau']))
    sigma_calculator = np.absolute(tau_true-tau_ave)/single_error_estimated_tau
    
    # Display the average estimated lifetime and its errors
    print('The error in the distribution of estimated lifetime calculated is {}'.format(single_error_estimated_tau))
    print('---------------------------------------------------------------------------------------------------------------')
    print('Average estimated lifetime for 500 simulations is {}'.format(tau_ave))
    print('The error in the estimated lifetime for 500 simulations is {}'.format(error_estimated_tau))
    print('---------------------------------------------------------------------------------------------------------------')
    print('The true lifetime is within {} sigma of the distribution of estimated lifetime for 500 simulations'.format(sigma_calculator))

    
    # Plotting data into subplots
    
    # Distribution of Muon Decaying Times
    pl.subplot(2, 2, 1)
    pl.title('Distribution of Muon Decaying Times', fontsize='x-large')
    pl.hist(np.array(data['x'])[:], facecolor='r', bins=50, ec='black')
    pl.xlabel(r'$Muon\/Decaying\/time\/in\/microseconds,\/\lambda/\mu s^{-1}$')
    pl.ylabel('Number of Muons')

	# Muon Lifetime Measurement
    pl.subplot(2, 2, 2)
    pl.title('Muon Lifetime Measurement', fontsize='x-large')
    pl.plot(np.array(data['x']), np.array(data['y-line']), 'ro', markersize=2.0)
    pl.axvline(tau_ave, 0, f_tau_ave, color='g', label = 'Estimated Lifetime')
    pl.axvline(tau_true, 0, f_tau_true, color='b', label = 'True Lifetime')
    pl.legend()
    pl.xlabel(r'$Muon\/Decaying\/time\/in\/microseconds,\/\lambda/\mu s^{-1}$')
    pl.ylabel(r'$Probability\/Density\/Function,\/P(\lambda)$')

	# Distribution of Estimated Tau Calculated
    pl.subplot(2, 1, 2)
    pl.title('Distribution of Estimated Tau Calculated', fontsize='x-large')
    pl.hist(np.array(data['estimated tau'], dtype=float), bins=50, ec='black')
    pl.xlabel('Estimated Tau')
    pl.ylabel('Number of Estimated Tau')

	# Display the subplots
    pl.subplots_adjust(hspace=0.6)
    pl.show()

main()

"""
Comments:

- Average estimated lifetime is lower than the true one because the number of muon decay rates within the first half is higher than that within the second half.

- In order to get an average estimate lifetime closer to true lifetime, increase the interval.

- Oversized interval could caused the random_x fn to be repeated infinitely because its hard to obtain a y random number for under the curve for bigger value of x, since its y value is too small.

- The true lifetime seems to be within 1 sigma of distribution of estimated lifetime calculated for 500 MC simulations

- The true lifetime also seems to be within 1 sigma of distribution of estimated lifetime calculated for a single MC simulation
"""
