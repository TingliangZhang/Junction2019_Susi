#include "mainwindow.h"
#include "ui_mainwindow.h"
#include"qfile.h"
#include"QTableWidgetItem"
#include"iostream"
#include"qtextstream.h"
#include"qmessagebox.h"
#include"qstring.h"
#include"QtCharts"
#include"qdebug.h"


using namespace std;
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connect(ui->tableWidget, SIGNAL(cellChanged(int row,int col)), this, SLOT(settingTableChanged(int row, int col)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked() //btn_refresh be clicked
{
    int emotionCount[8]={0,0,0,0,0,0,0,0};//the 8 emotions = {0:'Angry',1:'Fatigued',2:'Upset',3:'Anxious',4:'Tranquility',5:'Contented',6:'Joyful',7:'Excited',}

    //read the new file
    QString applicationDirPath;
    applicationDirPath = QCoreApplication::applicationDirPath();
    //qDebug()<<"applicationDirPath"<<applicationDirPath;
    QFile f(applicationDirPath+"/data.txt");
    if(!f.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        cout << "Open failed." << endl;
        return;
    }

    //refresh the list
    QTextStream txtInput(&f);
    QString lineStr;
    double emotionWeekMean[8]={0,0,0,0,0,0,0,0};
    int emotionWeekCount[8]={0,0,0,0,0,0,0,0};
    int headflag=0;

    while(!txtInput.atEnd())
    {
        QStringList strlist;
        QString strInsert;
        lineStr = txtInput.readLine();
        if(headflag==0)
        {
            headflag++;
            continue;
        }
        int row=ui->tableWidget->rowCount();
        ui->tableWidget->insertRow(row);
        QTableWidgetItem *check=new QTableWidgetItem;
        check->setCheckState (Qt::Unchecked);
        ui->tableWidget->setItem(row,0,check);
        strlist = lineStr.split('\t');
        for (int i=1;i<strlist.length();i++)
        {
            ui->tableWidget->setItem(row,i,new QTableWidgetItem(strlist[i]));
            emotionCount[strlist[2].toInt()]++;
        }
        strInsert = strlist[strlist.length()-2];
        ui->textBrowser->clear();
        ui->textBrowser->moveCursor(QTextCursor::End);
        ui->textBrowser->textCursor().insertText(strInsert) ;
        //from12 oneweek
        QStringList timeLis=strlist[1].split(' ');
        QStringList timeList=timeLis[0].split('-');
        emotionWeekCount[timeList[2].toInt()-12]++;
        emotionWeekMean[timeList[2].toInt()-12]+=strlist[2].toInt();
    }

    f.close();

    for(int i=0;i<8;i++)
    {
        if(emotionWeekCount[i])
        {
            emotionWeekMean[i]=emotionWeekMean[i]/emotionWeekCount[i]-3.5;
        }
        else
        {
            emotionWeekMean[i]=0;
        }
    }

    //draw time-emotion chart
    QList<QLineSeries *> m_series;
    QLineSeries *series1 = new QLineSeries();//实例化一个QLineSeries对象
    m_series.append(series1);
    series1->setName(QString("Emotion-Rate"));
    series1->setColor(QColor(0,0,0));
    series1->setVisible(true);
    series1->setPointLabelsVisible(true);
    series1->setPointLabelsColor(QColor(0,0,0));
    series1->setPointLabelsFormat("@yPoint");
    series1->setPointLabelsClipping(false);
    series1->setPointsVisible(true);
    for(int i=0;i<8;i++)
    {
        series1->append(i+12, emotionWeekMean[i]);
    }
    QChart *chart0 = new QChart();
    chart0->setAnimationOptions(QChart::AllAnimations);//设置启用或禁用动画
    chart0->addSeries(series1);
    chart0->createDefaultAxes();
    chart0->legend()->hide();
    chart0->axisX()->setRange(12,18);
    chart0->axisY()->setRange(-3.5,3.5);
    QChartView *chartview0 = new QChartView(this);
    chartview0->show();
    chartview0->setChart(chart0);


    if(ui->verticalLayout_2->count()!=0)
    {
        ui->verticalLayout_2->removeItem(ui->verticalLayout_2->itemAt(0));
    }
    ui->verticalLayout_2->insertWidget(0, chartview0);


    //draw piechart
    //the 8 emotions = {0:'Angry',1:'Fatigued',2:'Upset',3:'Anxious',4:'Tranquility',5:'Contented',6:'Joyful',7:'Excited',}
    QPieSlice *slice_0 = new QPieSlice(QStringLiteral("Angry"), emotionCount[0], this);
    slice_0->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_0->setBrush(QColor::fromRgb(138,40,33,225));
    QPieSlice *slice_1 = new QPieSlice(QStringLiteral("Fatigued"), emotionCount[1], this);
    slice_1->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_1->setBrush(QColor::fromRgb(188,203,202,225));
    QPieSlice *slice_2 = new QPieSlice(QStringLiteral("Upset"), emotionCount[2], this);
    slice_2->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_2->setBrush(QColor::fromRgb(6,3,68,225));
    QPieSlice *slice_3 = new QPieSlice(QStringLiteral("Anxious"), emotionCount[3], this);
    slice_3->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_3->setBrush(QColor::fromRgb(66,84,21,225));
    QPieSlice *slice_4 = new QPieSlice(QStringLiteral("Tranquility"), emotionCount[4], this);
    slice_4->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_4->setBrush(QColor::fromRgb(243,219,181,225));
    QPieSlice *slice_5 = new QPieSlice(QStringLiteral("Contented"), emotionCount[5], this);
    slice_5->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_5->setBrush(QColor::fromRgb(203,228,73,225));
    QPieSlice *slice_6 = new QPieSlice(QStringLiteral("Joyful"), emotionCount[6], this);
    slice_6->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_6->setBrush(QColor::fromRgb(252,233,78,225));
    QPieSlice *slice_7 = new QPieSlice(QStringLiteral("Excited"),emotionCount[7], this);
    slice_7->setLabelVisible(true); // 显示饼状区对应的数据label
    slice_7->setBrush(QColor::fromRgb(228,83,99,225));

    //将8个饼状分区加入series
    QPieSeries *series = new QPieSeries(this);
      series->append(slice_0);
      series->append(slice_1);
      series->append(slice_2);
      series->append(slice_3);
      series->append(slice_4);
      series->append(slice_5);
      series->append(slice_6);
      series->append(slice_7);

    QChart *chart = new QChart();
    chart->addSeries(series);
    chart->setAnimationOptions(QChart::AllAnimations); // 设置显示时的动画效果
    chart->legend()->hide();

    QChartView *chartview = new QChartView(this);
    chartview->show();
    chartview->setChart(chart);


    if(ui->verticalLayout->count()!=0)
    {
        ui->verticalLayout->removeItem(ui->verticalLayout->itemAt(0));
    }
    ui->verticalLayout->insertWidget(0, chartview);

    return;


}

void MainWindow::on_pushButton_2_clicked()
{
    ui->textBrowser_2->clear();
    QMessageBox::warning(NULL, "Warning", "Please be careful to share.");
    int row=ui->tableWidget->rowCount();
    for(int i=0;i<row;i++)
    {
        if(ui->tableWidget->item(i,0)->checkState()==Qt::Checked)
        {
            QString time=ui->tableWidget->item(i,1)->text();
            QString emotion=ui->tableWidget->item(i,3)->text();
            QString speech=ui->tableWidget->item(i,4)->text();

            ui->textBrowser_2->moveCursor(QTextCursor::End);
            ui->textBrowser_2->textCursor().insertText(time+", I felt "+emotion+" and recorded that "+speech+"."+"\n");
        }
    }
}
