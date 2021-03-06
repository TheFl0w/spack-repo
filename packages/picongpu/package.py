##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

import os


class Picongpu(Package):
    """PIConGPU: A particle-in-cell code for GPGPUs"""

    homepage = "https://github.com/ComputationalRadiationPhysics/picongpu"
    url      = "https://github.com/ComputationalRadiationPhysics/picongpu/archive/0.4.0.tar.gz"
    maintainers = ['ax3l']

    version('develop', branch='dev',
            git='https://github.com/ComputationalRadiationPhysics/picongpu.git')
    version('foilISAAC', branch='topic-20171114-foilISAAC',
            git='https://github.com/ax3l/picongpu.git')
    version('gtc18', branch='topic-NGCandGTC18',
            git='https://github.com/ax3l/picongpu.git')
    home = os.path.expanduser('~')
    version('local',
            git='file://{0}/src/picongpu'.format(home))
    # version('master', branch='master',
    #         git='https://github.com/ComputationalRadiationPhysics/picongpu.git')
    version('0.4.2',
            preferred=True,
            sha256='f02563f7e9af0e260a0e6a8b13651b982dc28ce4e44efacf1af3e4a39ded6958')
    version('0.4.1',
            sha256='e69c53282fa297f9aa9edf7671ef82b1c392a8163e6d990e9cc468c7fd85481a')
    version('0.4.0',
            sha256='ec29348dc2bc728725111ba927cbe9975ac917188c3d0882bf8c6dd8f0a3b83f')
    version('0.4.0-rc4',
            sha256='193ef717c634442053ac0b31aea6e7dfa3280eac5eb76e4ad840d17a29880eda')
    version('0.4.0-rc3',
            sha256='c50b4f7a0c3f83c0ffc00cec1c188513cf9a5306658ace02995460671e40b420')
    version('0.4.0-rc2',
            sha256='0b65fc17529f87f5a996c1ea3c13f9482e4c2e6d6a2abe5a5be7766a10cbfe6a')

    # Alpaka computing backends.
    # Accepted values are:
    #   cuda  - Nvidia CUDA (GPUs)
    #   omp2b - OpenMP 2.0 with grid-blocks parallel, sequential block-threads
    variant('backend', default='cuda',
            values=('cuda', 'omp2b'),
            multi=False,
            description='Control the computing backend')
    variant('cudacxx', default='nvcc',
            values=('nvcc', 'clang'),
            multi=False,
            description='Device compiler for the CUDA backend')
    variant('png', default=True,
            description='Enable the PNG plugin')
    variant('hdf5', default=True,
            description='Enable multiple plugins requiring HDF5')
    variant('adios', default=False,
            description='Enable the ADIOS plugin')
    variant('isaac', default=False,
            description='Enable the ISAAC plugin')

    # @TODO add type=('link, 'run') to all these?
    # @TODO define supported ranges instead of fixed versions
    depends_on('cmake@3.10.0:', type=['build', 'run'])
    depends_on('rsync', type='run')
    depends_on('util-linux', type='run', when='platform=darwin')  # GNU getopt
    depends_on('cuda@8.0:9.2', when='backend=cuda')
    depends_on('zlib@1.2.11')
    depends_on('boost@1.62.0:1.65.1 cxxstd=11')
    depends_on('boost@1.65.1 cxxstd=11', when='backend=cuda ^cuda@9:')
    # note: NOT cuda aware!
    # depends_on('mpi@2.3:', type=['link', 'run'])
    depends_on('openmpi@1.8:3.99', type=['link', 'run'])
    depends_on('pngwriter@0.7.0,develop', when='+png')
    depends_on('libsplash@1.7.0,develop', when='+hdf5')
    depends_on('adios@1.13.1:,develop', when='+adios')
    depends_on('isaac@1.4.0,develop', when='+isaac')
    depends_on('isaac-server@1.4.0,develop', type='run', when='+isaac')

    # shipped internal dependencies
    # @TODO get from extern!
    # alpaka, cupla, cuda-memtest, mallocMC, mpiInfo, CRP's cmake-modules

    # definitely unsupported compilers without sufficient C++11
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.8')
    conflicts('%clang@:7.3 platform=darwin')  # Xcode's AppleClang

    # NVCC host-compiler incompatibility list
    #   https://gist.github.com/ax3l/9489132
    conflicts('%gcc@5:', when='backend=cuda cudacxx=nvcc ^cuda@:7.5')
    conflicts('%gcc@5.4:', when='backend=cuda cudacxx=nvcc ^cuda@:8')
    conflicts('%gcc@5.6:', when='backend=cuda cudacxx=nvcc ^cuda@:9.1')
    conflicts('%gcc@8:', when='backend=cuda cudacxx=nvcc ^cuda@9.2:10')
    conflicts('%clang@:3.4,3.7:', when='backend=cuda cudacxx=nvcc ^cuda@7.5')
    conflicts('%clang@:3.7,4.0:', when='backend=cuda cudacxx=nvcc ^cuda@8:9.0')
    conflicts('%clang@:3.7,4.1:', when='backend=cuda cudacxx=nvcc ^cuda@9.1')
    conflicts('%clang@:3.7,5.1:', when='backend=cuda cudacxx=nvcc ^cuda@9.2')
    conflicts('%clang@:3.7,6.1:', when='backend=cuda cudacxx=nvcc ^cuda@10')
    conflicts('%intel@:14,16:', when='backend=cuda cudacxx=nvcc ^cuda@7.5')
    conflicts('%intel@:14,17:', when='backend=cuda cudacxx=nvcc ^cuda@8.0.44')
    conflicts('%intel@:14,18:', when='backend=cuda cudacxx=nvcc ^cuda@8.0.61:9')
    conflicts('%intel@:14,19:', when='backend=cuda cudacxx=nvcc ^cuda@10')

    # Clang compatibility with CUDA SDK
    conflicts('^cuda@:6.5', when='backend=cuda cudacxx=clang')
    conflicts('%clang@:3.8', when='backend=cuda cudacxx=clang')
    conflicts('%clang@3.9:5.0 ^cuda@9:', when='backend=cuda cudacxx=clang')
    conflicts('%clang@6.0 ^cuda@9.1:', when='backend=cuda cudacxx=clang')
    conflicts('%clang@7.0 ^cuda@10:', when='backend=cuda cudacxx=clang')

    def install(self, spec, prefix):
        path_bin = join_path(prefix, 'bin')
        path_etc = join_path(prefix, 'etc')
        path_include = join_path(prefix, 'include')
        path_lib = join_path(prefix, 'lib')
        path_share = join_path(prefix, 'share')

        install_tree('bin', path_bin)
        install_tree('buildsystem', join_path(prefix, 'buildsystem'))
        install_tree('etc', path_etc)
        install_tree('include', path_include)
        install_tree('lib', path_lib)
        install_tree('src', join_path(prefix, 'src'))
        install_tree('share', path_share)
        install_tree('thirdParty', join_path(prefix, 'thirdParty'))

        profile_in = join_path(os.path.dirname(__file__), 'picongpu.profile')
        profile_out = join_path(path_etc, 'picongpu')
        install(profile_in, profile_out)
        filter_file('@PIC_SPACK_COMPILER@', str(self.compiler.spec),
                    join_path(profile_out, 'picongpu.profile'))
        filter_file('@PIC_SPACK_ROOT@', str(os.environ['SPACK_ROOT']),
                    join_path(profile_out, 'picongpu.profile'))
        #filter_file('@PIC_SPACK_COMPILER@', str(self.compiler.spec),
        #            join_path(profile_out, 'picongpu.profile'))
        # spack load on concretized spec does not work right now, replace with
        # slightly non-concrete spec set a None-defaulted multi-variant to
        # work-around:
        # https://github.com/spack/spack/issues/6314
        spec_list = str(spec).split(' ')
        spec_list = list(filter(lambda x: not x.endswith('='), spec_list))
        sanitized_spec = ' '.join(spec_list)
        filter_file('@PIC_SPACK_SPEC@', sanitized_spec,
                    join_path(profile_out, 'picongpu.profile'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('PICSRC', self.prefix)
        run_env.set('PIC_EXAMPLES',
                    join_path(self.prefix, 'share/picongpu/examples'))
        run_env.set('PIC_PROFILE',
                    join_path(self.prefix, 'etc', 'picongpu',
                              'picongpu.profile'))
        if 'backend=cuda' in self.spec:
            run_env.set('PIC_BACKEND', 'cuda')
        elif 'backend=omp2b' in self.spec:
            run_env.set('PIC_BACKEND', 'omp2b')

        run_env.prepend_path('PATH',
                             join_path(self.prefix, 'bin'))
        run_env.prepend_path('PATH',
                             join_path(self.prefix, 'src/tools/bin'))
        run_env.prepend_path('PYTHONPATH',
                             join_path(self.prefix, 'lib/python'))
        # optional: default for TBG_SUBMIT, TBG_TPLFILE

        # pre-load depends
        #  https://github.com/LLNL/spack/issues/2378#issuecomment-316364232
        cmake_prefix_path = []
        include_path = []
        ld_library_path = []
        bin_path = []
        for x in self.spec.traverse():
            if str(x).startswith('icet'):
                cmake_prefix_path.append(x.prefix.lib)
            else:
                cmake_prefix_path.append(x.prefix)
            ld_library_path.append(x.prefix.lib)
            bin_path.append(x.prefix.bin)
            include_path.append(x.prefix.include)

        run_env.prepend_path('CMAKE_PREFIX_PATH', ':'.join(cmake_prefix_path))
        run_env.prepend_path('CPATH', ':'.join(include_path))
        run_env.prepend_path('LD_LIBRARY_PATH', ':'.join(ld_library_path))
        run_env.prepend_path('PATH', ':'.join(bin_path))
        # pre-load depending compiler
        cxx_bin = os.path.dirname(self.compiler.cxx)
        cxx_prefix = join_path(cxx_bin, '..')
        cxx_lib = join_path(cxx_prefix, 'lib')
        run_env.prepend_path('LD_LIBRARY_PATH', cxx_lib)
        run_env.prepend_path('PATH', cxx_bin)
        run_env.set('CC', self.compiler.cc)
        run_env.set('CXX', self.compiler.cxx)
