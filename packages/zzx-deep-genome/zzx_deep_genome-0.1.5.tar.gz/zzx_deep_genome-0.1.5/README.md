# zzz_deep_genome

一个辅助基因组学深度学习模型构建的函数库

A library of functions to assist in the construction of deep learning models for genomics.



## 主要功能（Key Features）

1、根据给定文件（bed、bigwig等）和条件（序列长度等），获取用于组学深度学习训练的训练集。

Obtain a training set for deep learning training in genomics based on a given file (bed, bigwig, etc.) and conditions (sequence length, etc.).



2、训练数据（label）的标准化。

Normalization of training data (label).



3、根据JASPAR数据库的pfms矩阵信息，构建用于初始化CNN的参数矩阵。

The parameter matrix for initializing the CNN is constructed based on the pfms matrix information from the JASPAR database.



4、获取一组或多组等长短序列对应的pfm、ppm、pwm矩阵。

Get the pfm, ppm, and pwm matrices corresponding to one or more sets of equal-length short sequences.



5、接收pfms列表，获取符合meme输入格式的文件



6、tensorflow(支持1.x和2.x)和pytorch(只支持1.x)模型1d卷积层的motif挖掘



7、调用染色质开放性深度学习模型



## 快速开始（Quick Start）

### 安装

```python
pip install zzx-deep-genome -i https://pypi.org/project/
```



### 获取训练数据集（Obtain training data set）

```python
from zzx_deep_genome.get_dataset import genome_dataset

genome_dataset(bed_path,fasta_path,seq_len=1024,
               genome_size_control=None,dataset_type='regression',
               bw_path=None,Data_Augmentation=False)
```



1、参数：

- bed_path：bed文件路径，指定用于构建数据集的样本。

  对分类任务，要求四列：chr、start、end、class

  对分类任务，要求三列：chr、start、end

- fasta_path：参考基因组路径

- seq_len：指定每个样本长度

  若bed文件中某样本的长度超过指定长度，则截取中间seq_len长度

  若bed文件中某样本的长度小于指定长度，则向两边扩展到seq_len长度

- genome_size_control：控制文件，如果指定该文件路径，则从根据seq_len截取（或扩展）出的样本中过滤掉不符合控制文件条件的样本。控制文件(指定染色体及其最大长度，列由TAB间隔)格式如下：

  ```
  chr01<TAB>1998644
  chr02<TAB>5783384
  ...
  chrn<TAB>6457466
  ```

  

- dataset_type：该模块支持对三种任务（classification、regression、base_regression）进行数据预处理，获取数据集。

- bw_path：对回归任务，需要给定对应bigwig文件路径，该模块将从bigwig文件中提取信号。

- Data_Augmentation：是否进行数据增强，若为True，则会使用反向互补序列进行数据增强。



2、返回结果

根据dataset_type的选择有不同返回：

- classification：返回一个三列的数据框，第一列为染色体号起止点等信息（即原始bed文件信息）、第二列为one-hot编码后的对应定长DNA序列，第三列为类别标签。
- regression：返回一个三列的数据框，第一列为染色体号起止点等信息（即原始bed文件信息）、第二列为one-hot编码后的对应定长DNA序列，第三列为对应序列上的平均信号值。
- base_regression：返回一个三列的数据框，第一列为染色体号起止点等信息（即原始bed文件信息）、第二列为one-hot编码后的对应定长DNA序列，第三列为对应序列上的信号值（每个碱基位置都有值）。



### 数据集（label）的标准化

``` python
from zzx_deep_genome.Standardization import bw_scale
bw_scale(in_path,out_path,standard=32)
```



1、参数

- in_path：输入（bigwig）文件路径
- out_path：输出（标准化后的bigwig）文件路径
- standard：高斯核的标准差



2、返回结果

标准化后的（bigwig）文件



### 根据JASPAR数据库先验信息进行CNN初始化

```python
from zzx_deep_genome.filter_initialization import filter_initialization_matrix

filter_initialization_matrix(taxonomic_groups='plants',data_local = None,
                                 filters=64,
                                 L_=8,
                                 pattern='ppm_rp25',
                                 background_acgt=[0.25, 0.25, 0.25, 0.25])
```



1、参数：

- taxonomic_groups：选择类群，目前只支持plants、fungi、vertebrates、insects

- data_local：本地文件（要求JASPAR PFMS格式）路径，若为None，则该模块将根据taxonomic_groups的设置，自动从JASPAR数据库下载对应文件到当前工作目录。

- filters：卷积滤波器的数目

- L_：卷积核的尺寸（对长度超过设定值的PFM，会根据信息熵筛选片段）

- pattern：模式，支持ppm_rp25（返回ppm矩阵每个位置减0.25后得到的均值为0的矩阵）、ppm（返回pp m矩阵）、pwm（返回pwm矩阵）

- background_acgt：计算pwm时需要的ACGT背景

  

2、返回结果

根据pattern的设置有不同返回：

- pattern = "ppm_rp25"，返回ppm矩阵每个位置减0.25后得到的均值为0的矩阵（可以尝试直接用于初始化）
- pattern = "ppm"，返回ppm矩阵
- pattern = "pwm"，返回pwm矩阵



### 获取pfm、ppm、pwm矩阵

```python
from zzx_deep_genome.get_pwm import get_pwm
get_pwm(file_path,background_acgt = [0.25,0.25,0.25,0.25],type_='pfm')
```



1、参数：

- file_path：输入文件路径，输入文件形如：

  ``` 
  >1
  ACTTTG
  ACCCCG
  ACCCTG
  
  >2
  AATAGCAAA
  AAATCCCGG
  AATTTCCCG
  ATCCCGGGA
  CGTTTGGGG
  ```

  

- background_acgt：计算pwm需要的ACGT背景

- type_：可选pfm、ppm、pwm，决定了最终的返回结果



2、返回结果

根据type_的设置有不同返回：

- pfm：返回pfm矩阵列表
- ppm：返回ppm矩阵列表
- pwm：返回pwm矩阵列表





### 获取meme格式的输入

``` python
from zzx_deep_genome.get_meme_file import get_pwm
get_meme_input_file(pfms_,meme_path)
```



1、参数

- pfms_：多个pfm矩阵（要求为numpy array格式）构成的列表或numpy array
- meme_path：输出文件路径



2、返回结果

meme格式的输入文件，形如：

```
MEME version 5.3.3

ALPHABET = ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF   motif_ppm0
letter-probability matrix: alength= 4 w= 10
0.0     0.060606062     0.93939394      0.0
0.45454547      0.21212122      0.33333334      0.0
0.54545456      0.0     0.09090909      0.36363637
0.0     0.060606062     0.121212125     0.8181818
0.121212125     0.18181819      0.0     0.6969697
0.42424244      0.121212125     0.0     0.45454547
0.060606062     0.24242425      0.0     0.6969697
0.121212125     0.0     0.0     0.8787879
0.09090909      0.8787879       0.0     0.030303031
0.18181819      0.030303031     0.3030303       0.4848485

MOTIF   motif_ppm1
letter-probability matrix: alength= 4 w= 22
0.21052632      0.39473686      0.39473686      0.0
0.05263158      0.7105263       0.078947365     0.15789473
0.05263158      0.078947365     0.55263156      0.31578946
0.0     0.9736842       0.02631579      0.0
0.34210527      0.15789473      0.02631579      0.47368422
0.0     1.0     0.0     0.0
0.13157895      0.84210527      0.02631579      0.0
0.0     0.0     0.94736844      0.05263158
0.0     0.05263158      0.94736844      0.0
0.0     0.8947368       0.0     0.10526316
0.0     0.0     1.0     0.0
0.28947368      0.0     0.6315789       0.078947365
0.2631579       0.23684211      0.42105263      0.078947365
0.02631579      0.81578946      0.15789473      0.0
0.21052632      0.0     0.7631579       0.02631579
0.2631579       0.0     0.5     0.23684211
0.0     0.18421052      0.5263158       0.28947368
0.05263158      0.05263158      0.55263156      0.34210527
0.39473686      0.39473686      0.13157895      0.078947365
0.02631579      0.36842105      0.18421052      0.42105263
0.81578946      0.078947365     0.05263158      0.05263158
0.078947365     0.23684211      0.65789473      0.02631579
```



### motif挖掘（tensorflow）

```python
from zzx_deep_genome.cnn_tf_motif_1d import get_tf_motif

get_tf_motif(meme_path,bed_file_path,fasta_file_path,model_path,
             seq_len,kernel_size,weight_name,weight_ ,genome_size_control_path,lim__         ,data_batch,all_batch,stochastic_control)

```



1、参数

- meme_path：输出文件（meme格式）路径
- bed_file_path：bed文件路径，即用于motif挖掘的序列
- fasta_file_path：参考基因组文件路径
- model_path：待挖掘的模型路径，必须以 "xxx/model_best.tf" 形式给出
- seq_len：确定用于motif挖掘的序列的长度（截取/扩展bed文件中指定的区间至定长）
- kernel_size：卷积核尺寸
- weight_name：需要挖掘的卷积层的名称（一般是第一层）
- weight_：卷积层权重矩阵（tensor形式），默认为None，若提供该参数，则model_path、weight_name可以给空字符串。
- genome_size_control_path：控制文件，如果指定该文件路径，则从根据seq_len截取（或扩展）出的样本中过滤掉不符合控制文件条件的样本。
- lim__：阈值，取值范围为 (0，1]
- data_batch：每一个batch的数据量
- all_batch：batch总量
- stochastic_control：是否对随机性进行控制，默认为False，若设置为True，则只有当 时，



2、返回结果

符合TOMTOM输入形式的motif挖掘结果，形如：

```
MEME version 5.3.3

ALPHABET = ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF	motif_ppm0
letter-probability matrix: alength= 4 w= 9
0.23708807	0.01038254	0.6403269	0.112202495
0.208512	0.7740051	0.015640056	0.0018428406
0.23585951	0.22998169	0.007329206	0.5268296
0.16168216	0.17603946	0.42579857	0.23647982
0.7104572	0.21738292	0.062801115	0.0093587395
0.060103104	0.6903967	0.2046878	0.044812344
0.23376372	0.13233523	0.26143044	0.37247062
0.32773656	0.0613678	0.58124757	0.029648054
0.28716996	0.0468479	0.39660218	0.26937994

MOTIF	motif_ppm1
letter-probability matrix: alength= 4 w= 9
0.540042	0.41781804	0.030677516	0.011462491
0.12956709	0.54485214	0.30183706	0.023743732
0.8500921	0.0020468733	0.13289325	0.014967762
0.2256422	0.34451437	0.021108381	0.40873504
0.006422065	0.79510796	0.16175418	0.03671579
0.26913828	0.5888855	0.022234162	0.119742095
0.14021082	0.0	0.24393614	0.615853
0.024153106	0.10712824	0.8687187	0.0
0.2454713	0.66579676	0.037381027	0.051350936


```





### motif挖掘（pytorch）

``` python
from zzx_deep_genome.cnn_torch_motif_1d import get_torch_motif

get_torch_motif(meme_path,bed_file_path,fasta_file_path,
                model_path,weight_name,filter_size,channel_num,
      seq_len,genome_size_control_path,lim__,data_batch,all_batch,stochastic_control=False)

```



1、参数

- channel_num：卷积核总数
- model_path：模型文件路径，形如 "xxx/best_model.pth.tar"
- 其他参数同  motif挖掘（tensorflow）



2、返回结果

符合TOMTOM输入形式的motif挖掘结果



### 模型调用

``` python
from zzx_deep_genome.tf_model import SE_Unet_1d
model = SE_Unet_1d()
```

