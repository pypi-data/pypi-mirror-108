
class world3D(object):

    def __init__(self, shape, world):

        assert world.size >= 8, ValueError("Must have at least 8 chunks for 3D load balancing.")

        target = shape / np.linalg.norm(shape)
        best = None
        bestFit = 1e20
        for i in range(2, int(world.size/2)+1):
            for j in range(2, int(world.size/i)):
                k = int(world.size/(i*j))
                nBlocks = np.asarray([i, j, k])
                total = np.prod(nBlocks)

                if total == world.size:
                    fraction = nBlocks / np.linalg.norm(nBlocks)
                    fit = np.linalg.norm(fraction - target)
                    if fit < bestFit:
                        best = nBlocks
                        bestFit = fit


        assert not best is None, Exception("Could not split {} into {} blocks. ".format(shape, world.size))

        self.xStarts, self.xChunkSizes = loadBalance1D_shrinkingArrays(shape[0], best[0])
        self.yStarts, self.ychunkSizes = loadBalance1D_shrinkingArrays(shape[1], best[1])
        self.zStarts, self.zChunkSizes = loadBalance1D_shrinkingArrays(shape[2], best[2])

        self.chunkShape = np.asarray([self.zChunks.size, self.yChunks.size, self.xChunks.size])
        self.chunkIndex = np.unravel_index(self.rank, self.chunkShape)

        self.world = world


    @property
    def xIndices(self):
        index = self.chunksIndex[2]
        i0 = self.xStarts[index]
        i1 = i0 + self.xChunkSizes[index]
        return np.s_[i0:i1]


    @property
    def yIndices(self):
        index = self.chunksIndex[1]
        i0 = self.yStarts[index]
        i1 = i0 + self.yChunkSizes[index]
        return np.s_[i0:i1]


    @property
    def zIndices(self):
        index = self.chunksIndex[0]
        i0 = self.zStarts[index]
        i1 = i0 + self.zChunkSizes[index]
        return np.s_[i0:i1]