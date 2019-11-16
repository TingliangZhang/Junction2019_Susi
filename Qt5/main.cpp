#include "mainwindow.h"
#include"qfile.h"
#include"iostream"
#include"qtextstream.h"

#include <QApplication>
using namespace std;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();

}
