import pandas as pd, numpy as np
from dorianUtils.configFilesD import ConfigDashTagUnitTimestamp
from dorianUtils.configFilesD import ConfigDashRealTime
from dorianUtils.configFilesD import ConfigDashSpark
import subprocess as sp, os,re,glob, datetime as dt
from dateutil import parser
from scipy import linalg,integrate
pd.options.mode.chained_assignment = None  # default='warn'

def removeMeteoDF(df):return df[~df.tag.str.contains('@SIS')]

'''difference between tags in df and dfPLC'''
def checkDiffbetweenPLCandDF(df,dfPLC):
    listTagsDf = pd.DataFrame(df.tag.unique(),columns=['tag'])
    listTagsDf = listTagsDf.sort_values(by='tag')
    dfplc=pd.DataFrame(dfPLC.TAG.sort_values())
    dfplc['id']='dfplc'
    listTagsDf['id']='listTagsDf'
    listTagsDf.columns=['TAG','id']
    return pd.concat([dfplc,listTagsDf],axis=0).drop_duplicates(subset='TAG',keep=False)

class ConfigFilesSmallPower(ConfigDashTagUnitTimestamp):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,folderPkl,folderFig=None,folderExport=None,encode='utf-8'):
        self.appDir = os.path.dirname(os.path.realpath(__file__))
        self.filePLC = glob.glob(self.appDir +'/confFiles/' + '*PLC*')[0]
        super().__init__(folderPkl,self.filePLC,folderFig=folderFig,folderExport=folderExport)
        # self.typeGraphs = pd.read_csv('confFiles/typeGraph.csv',index_col=0)
        self.usefulTags = pd.read_csv(self.appDir+'/confFiles/predefinedCategories.csv',index_col=0)
        self.usefulTags.index = self.utils.uniformListStrings(list(self.usefulTags.index))

        self.dfPLC      = self.__buildPLC(ds=False)
        self.legendTags = pd.read_csv(self.appDir+'/confFiles/tagLegend.csv')

    def __buildPLC(self,ds=True):
        if ds:return self.dfPLC[self.dfPLC.DATASCIENTISM==True]
        else : return self.dfPLC

    def _parkTag(self,df,tag,folder):
        # print(tag)
        dfTag=df[df.tag==tag]
        with open(folder + tag + '.pkl' , 'wb') as handle:
            pickle.dump(dfTag, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def parkDayPKL(self,datum,pool=False):
        print(datum)
        realDatum=parser.parse(datum)+dt.timedelta(days=1)
        df = self.loadFile('*'+ realDatum.strftime('%Y-%m-%d') + '*')
        if not df.empty:
            folder=folderPkl+'parkedData/'+ datum + '/'
            if not os.path.exists(folder):os.mkdir(folder)
            listTags=list(self.dfPLC.TAG.unique())
            if pool:
                with Pool(4) as p:p.starmap(self._parkTag,[(df,tag,folder) for tag in listTags])
            else:
                for tag in listTags:
                    self._parkTag(df,tag,folder)

    def parkDates(self,listDates,nCores=4):
        if nCores>1:
            with Pool(nCores) as p:
                p.starmap(self.parkDayPKL,[(datum,False) for datum in listDates])
        else :
            for datum in listDates:
                self.parkDayPKL(datum)

    def removeMeteoDF(self,df):
        return removeMeteoDF(df)
# ==============================================================================
#                   functions compute new variables
# ==============================================================================

    def integrateDFTag(self,df,tagname,timeWindow=60,formatted=1):
        dfres = df[df.Tag==tagname]
        if not formatted :
            dfres = self.formatRawDF(dfres)
        dfres = dfres.sort_values(by='timestamp')
        dfres.index=dfres.timestamp
        dfres=dfres.resample('100ms').ffill()
        dfres=dfres.resample(str(timeWindow) + 's').mean()
        dfres['Tag'] = tagname
        return dfres

    def integrateDF(self,df,pattern,**kwargs):
        ts = time.time()
        dfs = []
        listTags = self.getTagsTU(pattern[0],pattern[1])[self.tagCol]
        # print(listTags)
        for tag in listTags:
            dfs.append(self.integrateDFTag(df,tagname=tag,**kwargs))
        print('integration of pattern : ',pattern[0],' finished in ')
        self.utils.printCTime(ts)
        return pd.concat(dfs,axis=0)

    def DF_allPower(self,timeRange,melt=True,**kwargs):
        listPuissances = [k for k in list(self.usefulTags.index) if 'puissance' in k.lower()]
        listPuissances+=['Courant blowers','Courant pompes']
        dicPowerGroups = {k:self.getUsefulTags(k) for k in listPuissances}
        listTags = self.utils.flattenList(list(dicPowerGroups.values()))
        df = self.DF_loadTimeRangeTags(timeRange,listTags,**kwargs)

        #convert current pumps and blowers to power
        for k in dicPowerGroups['Courant blowers']:df[k]*=48
        for k in dicPowerGroups['Courant pompes']:df[k]*=24
        # for k in dicPowerGroups['Courant pompes']:df[k]*=24

        df=df.abs()# take absolute value of the power
        dfPtotal=df['SEH0.JT_01.HE10']
        del df['SEH0.JT_01.HE10']
        if melt:
            df['timestamp'] = df.index
            df=df.melt(id_vars='timestamp')

            PowerGroup = self.utils.flattenDict([{l:k for l in self.getUsefulTags(k)} for k in listPuissances])
            PowerGroup = {k:'puissance '+' '.join(v.split()[1:]) for k,v in PowerGroup.items()}
            df['PowerGroup'] = [PowerGroup[k] for k in df.tag]
            #
            legendDict = {self.legendTags.iloc[k,0]:self.legendTags.iloc[k,2] for k in range(len(self.legendTags))}
            df['legend'] = [legendDict[k] for k in df.tag]
        return df,dfPtotal,dicPowerGroups

    def getUsefulTags(self,usefulTag='puissance chauffant GV'):
        category = self.usefulTags.loc[usefulTag]
        return self.getTagsTU(category.Pattern,category.Unit)

    def getTagsUsedForPower(self):
        tagList,dfs = list(self.dictPower.keys())[:-1],[]
        for group in tagList:
            pat = self.dictPower[group]
            df = self.getTagsTU(pat[0],pat[1])
            df['group'] = group
            if len(pat)==3 :
                df['voltage'] = pat[2]
            else :
                df['voltage'] = np.nan
            dfs.append(df)
        res = pd.concat(dfs)
        res.to_csv('variableUsedToComputePower.csv')
        # self.utils.printDFSpecial(res)
        return res

    def plotGraphPowerArea(self,timeRange,expand=False,groupnorm='',**kwargs):
        import plotly.express as px
        import plotly.graph_objects as go
        df,dfPtotal,dicPowerGroups = self.DF_allPower(timeRange,melt=True,**kwargs)

        if expand :fig=px.area(df,x='timestamp',y='value',color='tag',groupnorm=groupnorm)
        else : fig=px.area(df,x='timestamp',y='value',color='PowerGroup',groupnorm=groupnorm,line_group='tag')

        traceP=go.Scatter(x=dfPtotal.index,y=dfPtotal,name='SEH0.JT_01.HE10',mode='lines+markers',
                                marker=dict(color='blue'))
        fig.add_trace(traceP)

        return fig

    # ==============================================================================
    #                   functions computation
    # ==============================================================================

    def prepareDFforFit(self,filename,ts=None,group='temperatures Stack 1',rs='30s'):
        df = self.loadFile(filename)
        a  = self.usefulTags[group]
        df = self.getDFTagsTU(df,a[0],a[1])
        df = self.pivotDF(df,resampleRate=rs)
        if not not ts :
            df= self.getDFTime(df,ts)
        return df

    def fitDataframe(self,df,func='expDown',plotYes=True,**kwargs):
        res = {}
        period = re.findall('\d',df.index.freqstr)[0]
        print(df.index[0].freqstr)
        for k,tagName in zip(range(len(df)),list(df.columns)):
             tmpRes = self.utils.fitSingle(df.iloc[:,[k]],func=func,**kwargs,plotYes=plotYes)
             res[tagName] = [tmpRes[0],tmpRes[1],tmpRes[2],
                            1/tmpRes[1]/float(period),tmpRes[0]+tmpRes[2]]
        res  = pd.DataFrame(res,index = ['a','b','c','tau(s)','T0'])
        return res

class ConfigFilesSmallPowerSpark(ConfigDashSpark):
    def __init__(self,sparkData,sparkConfFile,confFile=None,folderFig=None,folderExport=None,encode='utf-8'):
        self.appDir = os.path.dirname(os.path.realpath(__file__))
        if not confFile : confFile=glob.glob(self.appDir +'/confFiles/' + '*PLC*')[0]
        super().__init__(sparkData,sparkConfFile,confFile=confFile,folderFig=folderFig,folderExport=folderExport)
        self.usefulTags = pd.read_csv(self.appDir+'/confFiles/predefinedCategories.csv',index_col=0)
        self.dfPLC = self.__buildPLC()

    def __buildPLC(self):
        return self.dfPLC[self.dfPLC.DATASCIENTISM==True]

class ConfigFilesSmallPower_RealTime(ConfigDashRealTime):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,confFolder,timeWindow=2*60*60,
                    folderFig=None,folderExport=None,encode='utf-8'):
        self.appDir  = os.path.dirname(os.path.realpath(__file__))
        self.filePLC = glob.glob(self.appDir +'/confFiles/' + '*PLC*')[0]
        self.connParameters ={
            'host'     : "192.168.1.222",
            'port'     : "5434",
            'dbname'   : "Jules",
            'user'     : "postgres",
            'password' : "SylfenBDD"
        }
        super().__init__(confFolder,timeWindow,self.connParameters,
                            folderFig=folderFig,folderExport=folderExport)

    def connectToJulesDataBase(self,connParameters=None):
        if not connParameters :
            connParameters ={
                'host'     : "192.168.1.222",
                'port'     : "5434",
                'dbname'   : "Jules",
                'user'     : "postgres",
                'password' : "SylfenBDD"
            }
        connReq = self.utils.connectToPSQLsDataBase(connParameters)
        return conn

class AnalysisPerModule(ConfigFilesSmallPower):
    def __init__(self,folderPkl,folderFig=None,folderExport=None,encode='utf-8'):
        super().__init__(folderPkl,folderFig,folderExport,encode)
        self.modules=self._loadModules()
        self.listModules=list(self.modules.keys())

    def _buildEauProcess(self):
        eauProcess={}
        eauProcess['pompes']=['PMP_04','PMP_05']
        eauProcess['TNK01'] = ['L219','L221','L200','L205','GWPBC_TNK_01']
        eauProcess['pompe purge'] = ['GWPBC_PMP_01','L202','L210']
        eauProcess['toStack'] = ['L036','L020','GFD_01']
        return eauProcess

    def _buildGV(self):
        GV = {}
        GV['GV1'] = ['L211','L213_H2OPa','STG_01a']
        GV['GV2'] = ['L211','L213_H2OPb','STG_01b']
        return GV

    def _buildValo(self):
        Valo = {}
        Valo['amont-retour'] = ['GWPBC_PMP_02','L400','L416','L413']
        Valo['echangeur 1'] = ['HPB_HEX_01','L402','L114','L117']
        Valo['condenseur 1'] = ['HPB_CND_01','L408','L404','L021','L022']
        Valo['echangeur 2'] = ['HPB_HEX_02','L404','L115','L116']
        Valo['condenseur 2'] = ['HPB_CND_02','L406','L046','L045']
        Valo['batiment'] = ['GWPBC-HEX-01','L414','L415']
        return Valo

    def _buildGroupeFroid(self):
        groupFroid = {}
        groupFroid['groupe froid'] = ['HPB_CND_03','L417','L418','L056','L057']

    def _loadModules(self):
        modules = {}
        modules['eau process']=self._buildEauProcess()
        modules['GV']=self._buildGV()
        modules['groupe froid']=self._buildGroupeFroid()
        modules['valo']=self._buildValo()
        return modules

    def _categorizeTagsPerUnit(self,module):
        '''module : {'eauProcess',} given by self.listModules'''
        mod=self.modules[module]
        ll = self.utils.flattenList([self.listTagsModule(mod,g)[1] for g in mod])
        dfPLC1 = self.dfPLC[self.dfPLC.TAG.isin(ll)]
        unitGroups={}
        for u in dfPLC1.UNITE.unique():
            unitGroups[u]=list(dfPLC1[dfPLC1.UNITE==u].TAG)
        return unitGroups


    # ==========================================================================
    #                           functions
    # ==========================================================================
    def listTagsModule(self,module,group):
        groupList=module[group]
        lplc=pd.concat([self.getTagsTU(pat,ds=False,cols='tdu') for pat in groupList])
        lds=self.utils.flattenList([self.getTagsTU(pat,ds=True) for pat in groupList])
        return lplc,lds

    def listTagsAllModules(self,module):
        mod=self.modules[module]
        LPLC = {g:self.listTagsModule(mod,g)[0] for g in mod}
        LDS = {g:self.listTagsModule(mod,g)[1] for g in mod}
        return LPLC,LDS

    def figureModuleUnits(self,module,timeRange,grid=None,**kwargs):
        from plotly.subplots import make_subplots
        unitGroups=self._categorizeTagsPerUnit(module)
        if not grid:grid=self.utils.optimalGrid(len(unitGroups))
        fig = make_subplots(rows=grid[0], cols=grid[1])
        rows,cols=self.utils.rowsColsFromGrid(len(unitGroups),grid)
        for k,r,c in zip(unitGroups.keys(),rows,cols):
            print(k)
            listTags = unitGroups[k]
            df = self.DF_loadTimeRangeTags(timeRange,listTags,rs='auto',**kwargs)
            df=df.ffill().bfill()
            for l in df.columns:
                fig.add_scatter(y=df[l],x=df.index, mode="lines",
                                hovertemplate='<b>%{y:.1f}',
                                name=l, row=r, col=c)
            fig.update_yaxes(title_text=self.utils.detectUnit(k) + ' in '+ k, row=r, col=c)
        fig.update_xaxes(matches='x')
        fig.update_layout(title={"text": module})
        return fig

    def plotQuick(self,df,duration='short',title='',form='df'):
        df=df.ffill().bfill()
        if form=='step': plt.step(x=df.index,y=df.iloc[:,0],)
        if form=='multi': mpl.multiYmpl(df)
        if form=='df': df.plot(colormap='jet')
        datenums=md.date2num(df.index)
        if duration=='short': xfmt = md.DateFormatter('%H:%M')
        else: xfmt = md.DateFormatter('%b-%d')
        ax=plt.gca()
        plt.xticks( rotation=25 )
        # ax.xaxis.set_major_formatter(xfmt)
        # ax.set_ylabel('timestamp')
        mpl.plt.title(title)

    def checkDFvsPLCTags(self,df):
        df2=df.tag.unique()
        df2.columns='TAG'
        dupl = pd.concat([df2,self.dfPLC.TAG]).duplicated(subset=['TAG'])
        return dupl
