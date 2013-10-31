hadoop dfs -rmr liveOutput
hadoop dfs -rmr tinyOutput
hadoop jar giraph.jar  org.apache.giraph.GiraphRunner  test.LiveJournalPageRank -mc test.LiveJournalPageRank\$SimplePageRankVertexMasterCompute -eif org.apache.giraph.io.formats.IntNullTextEdgeInputFormat  -eip live.txt   -of org.apache.giraph.io.formats.IdWithValueTextOutputFormat  -op liveOutput   -w 4
