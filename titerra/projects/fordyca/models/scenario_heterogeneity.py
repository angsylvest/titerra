# Copyright 2022 Angel Sylvester, John Harwell, All rights reserved.
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
import statistics
import typing as tp
import os

# 3rd party packages

# Project packages
from sierra.core import vector, types
from sierra.core.utils import ArenaExtent
from sierra.core.experiment_spec import ExperimentSpec
import titerra.projects.fordyca.models.representation as rep 


class Calculator:
    # Calculates the heterogenity of a scenario w.r.t a reference version.

    def __init__(self, scenario: str) -> None:
        self.scenario = scenario

    def from_results(self,
        main_config: types.YAMLDict,
        cmdopts: types.Cmdopts,
        spec: ExperimentSpec, nest: rep.Nest) -> float:
        # We calculate per-run, rather than using the averaged block cluster
        # results, because for power law distributions different simulations
        # have different cluster locations, which affects the distribution via
        # locality.
        #
        # For all other block distributions, we can operate on the averaged
        # results, because the position of block clusters is the same in all
        # runs.

        if 'PL' in cmdopts['scenario']:
            result_opaths = [os.path.join(cmdopts['exp_output_root'],
                                        d,
                                          main_config['sim']['sim_metrics_leaf'])
                                          for d in os.listdir(cmdopts['exp_output_root'])]
        else:
            result_opaths = [os.path.join(cmdopts['exp_stat_root'])]

        # nest = rep.Nest(cmdopts, spec)

        heterogeneity = 0.0

        for result in result_opaths:
            clusters = rep.BlockClusterSet(cmdopts, nest, result)
            heterogeneity += self.from_clusters(clusters, spec.arena_dim, cmdopts, spec, nest)

        avg_hetero = heterogeneity / len(result_opaths)

        return avg_hetero


    def from_clusters(self,
                  clusters: rep.BlockClusterSet,
                  arena: ArenaExtent, cmdopts: types.Cmdopts,
                  spec: ExperimentSpec, nest: rep.Nest ) -> float:
        clusters_l = list(clusters)

        arena_dims = nest.arena_dim
        diagonal = math.sqrt(arena_dims.xsize()**2 +  arena_dims.ysize()**2)

        # nest = rep.Nest(cmdopts, spec)
        nest_x, nest_y = nest.extent.center.x, nest.extent.center.y

        if 'SS' in self.scenario:
            cx, cy = list(clusters.clusters)[0].cluster_center
            # IMPORTANT NOTE: this value is the nest center
            nest_x, nest_y = nest_x, nest_y
            dist = math.sqrt((cx - nest_x)**2 + (cy - nest_y)**2)
            return (dist / diagonal)*(arena_dims.xsize()**(0.1))*0.055


        elif 'DS' in self.scenario:
            c0_center = list(clusters.clusters)[0].cluster_center
            c1_center = list(clusters.clusters)[1].cluster_center

            leftx, lefty = nest_x, nest_y
            cx1, cy1 = list(clusters.clusters)[0].cluster_center
            cx2, cy2 = list(clusters.clusters)[1].cluster_center
            left_calc = math.sqrt((cx1 - leftx) ** 2 + (cy1 - lefty) ** 2)
            right_calc = math.sqrt((cx2 - leftx) **2 + (cy2 - lefty) ** 2)
            return (((left_calc + right_calc) / 2) / diagonal)*(arena_dims.xsize()**(0.1))*0.055

        variance = Calculator._variance_calc(clusters)
        nearest_neighbors = Calculator._nn_calc(clusters)
        mean_neighbor = [statistics.mean(i) for i in zip(*nearest_neighbors)]
        return ((0.055)*arena_dims.xsize()**(0.75)*((statistics.mean(mean_neighbor)/diagonal))*2**(variance/diagonal))
       # return ((0.055)*arena_dims.xsize()**(0.85)*((statistics.mean(mean_neighbor)/diagonal)*2**(variance/diagonal)



    @staticmethod
    def _variance_calc(clusters: rep.BlockClusterSet) -> float:
        """
        This will calculate the variance for the distances measured for each cluster
        and will be probably be a scaled metric to be integrated into the
        existing PDF
        """

        nearest_neighbors = Calculator._nn_calc(clusters)

        # this is an array of variance of each neighbor, ordered from least to
        # greatest distance
        complete_variance = [statistics.variance(i) for i in zip(*nearest_neighbors)]

        return statistics.mean(complete_variance)

    @staticmethod
    def _nn_calc(clusters: rep.BlockClusterSet) -> tp.List[tp.List[vector.Vector3D]]:


        ret = []

        for outer in clusters:
            nearest_neighbors = []
            nearest_distance = []

            x,y = outer.cluster_center

            for inner in clusters:

                if inner == outer:
                    continue

                x_indiv, y_indiv = inner.cluster_center

                dist = math.sqrt((x_indiv - x)**2 + (y_indiv - y)**2)

                if len(nearest_neighbors) < 3:
                    nearest_neighbors.append(inner.cluster_center)
                    nearest_distance.append(dist)
                else:
                    if min(nearest_distance) > dist:
                        index = nearest_distance.index(max(nearest_distance))
                        nearest_distance[index] = dist
                        nearest_neighbors[index] = inner.cluster_center

                        # nearest_neighbors[inner.cluster_center] = nearest_distance
            # so that variance comparisons compare similar neighbors
            nearest_distance.sort()
            ret.append(nearest_distance)

        return ret
