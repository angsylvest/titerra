# Copyright 2021 John Harwell, All rights reserved.
#
#  This file is part of SIERRA.
#
#  SIERRA is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  SIERRA is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  SIERRA.  If not, see <http://www.gnu.org/licenses/

# Core packages
import math

# 3rd party packages

# Project packages
import sierra.core.variables.time_setup as ts


def crwD_for_searching(N: float,
                       wander_speed: float,
                       ticks_per_sec: int,
                       scenario_hetero: float,
                       scenario: str) -> float:
    """
    Approximates the diffusion constant in a swarm of N CRW robots for bounded arena geometry for
    when searching. From :xref:`Harwell2021b`, inspired by the results in :xref:`Codling2010`.
    Note: for each scenario, constants derived from heterogeneity_calc.py were 
    used to find a line a best fit (using the original fitted values) 
    """
    tick_len = 1.0 / ticks_per_sec

    # 0.055 is what you get if you solve the Codling2010 integral with a range of [-5,5]
    # degrees rather than [-pi,pi].
    drift_xy = wander_speed ** 2 / (4 * tick_len) * 1.0 / 0.055

    if 'RN' in scenario:
        # ODE-3 small const-rho,var-rho (ORIGINAL) 
        # L_s = 0.055 * 1.5 * (math.sqrt(2.0))

        # ODE-3 small (with heterogeneity), var-rho
        # L_s = 0.143 # 0.14

        # ODE-3 small (with heterogeneity), const-rho 
        # L_s = 0.162

        # ODE-3 large const-rho
        # L_s = 0.055 * (3.75 * math.sqrt(2.0))

        # ODE-3 large var-rho
        # L_s = 0.055 * (3.5 * math.sqrt(2.0))

        # ODE-3 large (with heterogeneity), var-rho
        # L_s = 0.252

        # ODE-3 large (with heterogeneity), const-rho
        L_s = scenario_hetero

    elif 'PL' in scenario:
        # ODE-3 small const-rho
        # L_s = 0.055 / (math.sqrt(2.0))

        # ODE-3 small var-rho(ORIGINAL) 
        # L_s = 0.055 / (3.75 * math.sqrt(2.0))
  
        # ODE-3 small (with heterogenity), var-rho 
        # L_s = (-0.291*0.448534) + 0.143

        # ODE-3 small (with heterogeneity), const-rho
        # L_s = 0.162 + (-0.27*0.4164616457)

        # ODE-3 large const-rho
        # L_s = 0.055 * (4.0 * math.sqrt(2.0))

        # ODE-3 large var-rho
        # L_s = 0.055 * (3.0 * math.sqrt(2.0))

        # ODE-3 large (with heterogeneity), var-rho 
        # L_s = 0.252 + (-0.318*0.004643971069)

        # ODE-3 large (with heterogenity), const-rho
        # L_s = 0.288 + (-0.302*0.004643971069)

        L_s = scenario_hetero
    elif 'DS' in scenario:
        # ODE-3 small const-rho (ORIGINAL)
        # L_s = 0.055 * (1.5 * math.sqrt(2.0))

        # ODE-3 small (with heterogenity), var-rho
        # L_s = (-0.291*0.1980694901) + 0.143

        # ODE-3 small (with heterogeneity), const-rho
        # L_s = 0.162 + (-0.27*0.1980694901)

        # ODE-3 small var-rho
        # L_s = 0.055 * (math.sqrt(2.0))

        # ODE-3 large const-rho
        # L_s = 0.055 * (2.75 * math.sqrt(2.0))

        # ODE-3 large var-rho
        # L_s = 0.055 * 2.5 * (math.sqrt(2.0))
   
        # ODE-3 large (with heterogeneity), var-rho
        # L_s = 0.252 + (-0.318*0.1980694901)

        # ODE-3 large (with heterogeneity), const-rho
        # L_s = 0.288 + (-0.302*0.1980694901)

        L_s = scenario_hetero
    elif 'SS' in scenario:
        # ODE-3 small const-rho
        # L_s = 0.055 * 2 * math.sqrt(2.0)

        # ODE-3 small (with heterogeneity), var-rho
        # L_s = (-0.291*0.1222849675) + 0.143

        # ODE-3 small (with heterogeneity), const-rho
        # L_s = 0.162 + (-0.27*0.1222849675)

        # ODE-3 small var-rho
        # L_s = 0.055 * math.sqrt(2.0)

        # ODE-3 large const-rho
        # L_s = 0.055 * 2.5 * math.sqrt(2.0)

        # ODE-3 large var-rho
        # L_s = 0.055 * 2.0 * math.sqrt(2.0)

        # ODE-3 large (with heterogeneity), var-rho  
        # L_s = 0.252 + (-0.318*0.1222849675)

        # ODE-3 large (with heterogeneity), const-rho
        # L_s = 0.288 + (-0.302*0.1222849675)

        L_s = scenario_hetero
    F_N = N * drift_xy * L_s
    return F_N


def crwD_for_avoiding(N: float, wander_speed: float, ticks_per_sec: int, scenario_hetero: float, scenario: str) -> float:
    """
    Approximates the diffusion constant in a swarm of N CRW robots for bounded arena geometry for
    collision avoidance. From :xref:`Harwell2021b`, inspired by the results in :xref:`Codling2010`.

    """
    D = crwD_for_searching(N, wander_speed, ticks_per_sec, scenario_hetero, scenario) * 1.0 / 0.055

    if 'PL' in scenario:
        # ODE-3 small const-rho
        # return D / (math.sqrt(2.0))

        # ODE-3 small var-rho (tested for small)
        # return D * (10 * math.sqrt(2.0))

        # ODE-3 large const-rho
        return D / (4.0 * math.sqrt(2.0))

        # ODE-3 large var-rho
        # return -D / (1200 * math.sqrt(2.0))
    elif 'RN' in scenario:
        # ODE-3 small const-rho,var-rho (tested for small) 
        # return D * 2.5 * (math.sqrt(2.0))

        # ODE-3 large const-rho
        return D / (1.75 * math.sqrt(2.0))

        # ODE-3 large var-rho
        # return -D / (2400 * math.sqrt(2.0))

    elif 'DS' in scenario:
        # ODE-3 small const-rho (tested for small)
        # return D / (1.5 * math.sqrt(2.0))

        # ODE-3 small var-rho
        # return D

        # ODE-3 large const-rho
        return D / (4.75 * math.sqrt(2.0))

        # ODE-3 large var-rho
        # return D / (22.5 * math.sqrt(2.0))

    elif 'SS' in scenario:
        # ODE-3 small const-rho (tested for small)
        # return D / (2.0 * math.sqrt(2.0))

        # ODE-3 small var-rho
        # return D / (math.sqrt(2.0))

        # ODE-3 large const-rho
        return D / (8.5 * math.sqrt(2.0))

        # ODE-3 large var-rho
        # return D / (45 * math.sqrt(2.0))

