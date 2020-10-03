import java.util.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.io.*;


public class GUI extends JFrame {
  private GraphPanel graphPanel;
  private StatusBar statusBar;


  private int[] selectionBounds = new int[2];
  private int viewFrom;

  private JMenuBar menuBar;
  private JMenu fileMenu;
  private JMenu plotMenu;
  private JMenu calcMenu;


  private JMenuItem openMenuItem;
  private JMenuItem saveMenuItem;
  private JMenuItem loadMenuItem;

  private JMenuItem psdMenuItem;
  private JMenuItem autocorrMenuItem;
  private JMenuItem histMenuItem;
  private JMenuItem signalMenuItem;


  private JMenuItem stdMenuItem;
  private JMenuItem entropMenuItem;

  private int chNumber;
  private CheckBoxList checkPanel;

  private ArrowListener arrowListener;
  private float[][]ys;
  private String[] labels;

  private EEGData myData;

  public GUI(Observer observer, EEGData eegData, ProjectManager projObj){
    myData = eegData;
    ys = myData.getSignal();
    labels = myData.getLabels();

    chNumber = ys.length;
    System.out.println("CH number: " + chNumber);

    setVisible(true);
    setResizable(false);
    //setPreferredSize(900,700);
    //setLayout(new GridLayout(0,1));
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    MenuitemListener itemListener = new MenuitemListener();
    itemListener.setObserver(observer);
    itemListener.setProjectManager(projObj);


    checkPanel = new CheckBoxList(labels,itemListener);


    observer.setBounds(0,0);
    graphPanel = new GraphPanel(observer,ys,labels);
    graphPanel.drawGraphs(checkPanel.getChecks());

    statusBar = new StatusBar();

    menuBar      = new JMenuBar();

    fileMenu     = new JMenu("File");
    plotMenu     = new JMenu("Plot");
    calcMenu     = new JMenu("Calculate");



    openMenuItem = new JMenuItem("Open");
    saveMenuItem = new JMenuItem("Save");
    loadMenuItem = new JMenuItem("Load EDF");

    psdMenuItem  = new JMenuItem("Power Spectrum");
    autocorrMenuItem = new JMenuItem("Autocorrelation");
    histMenuItem = new JMenuItem("Histogram");
    signalMenuItem = new JMenuItem("Signal");



    stdMenuItem  = new JMenuItem("Standard Deviation");
    entropMenuItem = new JMenuItem("Entropy");


    openMenuItem.setActionCommand("open");
    saveMenuItem.setActionCommand("save");
    loadMenuItem.setActionCommand("load");

    psdMenuItem.setActionCommand("PSD");
    autocorrMenuItem.setActionCommand("AC");
    histMenuItem.setActionCommand("HIST");;
    signalMenuItem.setActionCommand("SIG");

    stdMenuItem.setActionCommand("STD");
    entropMenuItem.setActionCommand("ENTROP");




    openMenuItem.addActionListener(itemListener);
    saveMenuItem.addActionListener(itemListener);
    loadMenuItem.addActionListener(itemListener);

    psdMenuItem.addActionListener(itemListener);
    autocorrMenuItem.addActionListener(itemListener);
    histMenuItem.addActionListener(itemListener);
    signalMenuItem.addActionListener(itemListener);


    stdMenuItem.addActionListener(itemListener);
    entropMenuItem.addActionListener(itemListener);

    arrowListener = new ArrowListener();
    addKeyListener(arrowListener);

    setFocusable(true);
    requestFocusInWindow();


    fileMenu.add(openMenuItem);
    fileMenu.add(saveMenuItem);
    fileMenu.add(loadMenuItem);

    plotMenu.add(psdMenuItem);
    plotMenu.add(autocorrMenuItem);
    plotMenu.add(histMenuItem);
    plotMenu.add(signalMenuItem);


    calcMenu.add(stdMenuItem);
    calcMenu.add(entropMenuItem);

    menuBar.add(fileMenu);
    menuBar.add(plotMenu);
    menuBar.add(calcMenu);

    setJMenuBar(menuBar);

    JPanel mainPanel = new JPanel();
    mainPanel.add(checkPanel);
    mainPanel.add(graphPanel);

    getContentPane().setLayout(
      new BoxLayout(getContentPane(), BoxLayout.Y_AXIS)
    );


    add(mainPanel);
    add(statusBar);
    pack();


  }
  private class MenuitemListener implements ActionListener{
    private Observer obs;
    private ProjectManager projObj;
    public void actionPerformed(ActionEvent event){
      if(event.getActionCommand() == "open"){
        System.out.println("Open project file!");
        statusBar.loadingProject();
        JFileChooser fileChooser = new JFileChooser();
        int i = fileChooser.showOpenDialog(graphPanel);

        if(i==JFileChooser.APPROVE_OPTION){



          File f = fileChooser.getSelectedFile();
          String filePath = f.getAbsolutePath();

          projObj.load_project(filePath);
          String edfPath   = projObj.getPath();
          boolean[] actchs = projObj.getChannels();
          int[] selBounds  = projObj.getSelection();

          myData.reloadData(edfPath);
          graphPanel.reloadGraphs(myData.getSignal(),myData.getLabels());
          graphPanel.setViewFrom(projObj.getViewpos());
          graphPanel.setSignalHeight(projObj.getSigHeight());
          graphPanel.setZoomMultiplier(projObj.getZoom());
          graphPanel.setSelectionBounds(selBounds[0],selBounds[1]);

          checkPanel.setChecks(actchs);
          graphPanel.drawGraphs(checkPanel.getChecks());
          requestFocusInWindow();
          repaint();
          System.out.println("Loading done!");
          statusBar.ready();
        }
      }

      if(event.getActionCommand() == "save"){
        String edfpth    = myData.getPath();
        boolean[] actChs = checkPanel.getChecks();
        int viewp = graphPanel.getViewFrom();
        int zoom  = graphPanel.getZoomMultiplier();
        int selFr = graphPanel.getRelativeSelection()[0];
        int selTo = graphPanel.getRelativeSelection()[1];
        int sigH  = graphPanel.getSignalHeight();
        System.out.println("Save project file!");
        JFileChooser fileChooser = new JFileChooser();
        int i = fileChooser.showSaveDialog(graphPanel);
        if(i==JFileChooser.APPROVE_OPTION){
          File f = fileChooser.getSelectedFile();
          String filePath = f.getAbsolutePath();
          System.out.println("File to save: "+filePath);
          projObj.save_project(filePath,edfpth,actChs,viewp,zoom,selFr,selTo,sigH);
        }
      }

      if(event.getActionCommand() == "load"){
        System.out.println("Load EDF data!");
        statusBar.loadingEDF();
        JFileChooser fileChooser = new JFileChooser();
        int i = fileChooser.showOpenDialog(graphPanel);
        if(i==JFileChooser.APPROVE_OPTION){
          File f = fileChooser.getSelectedFile();
          String filePath = f.getAbsolutePath();
          System.out.println("File to load: "+filePath);
          myData.reloadData(filePath);
          System.out.println("Java data reload done!");
          graphPanel.reloadGraphs(myData.getSignal(),myData.getLabels());
          graphPanel.drawGraphs(checkPanel.getChecks());
          requestFocusInWindow();
          repaint();
          statusBar.ready();
        }
      }

      if(event.getActionCommand() == "PSD"){
        System.out.println("Plot PSD!");
        selectionBounds = graphPanel.getSelectionBounds();
        obs.setBounds(selectionBounds[0],selectionBounds[1]);
        obs.setActiveChannels(checkPanel.getChecks());
        obs.notif("PLOT PSD");

      }
      if(event.getActionCommand() == "AC"){
        System.out.println("Plot autocorrelation!");
        selectionBounds = graphPanel.getSelectionBounds();
        obs.setBounds(selectionBounds[0],selectionBounds[1]);
        obs.setActiveChannels(checkPanel.getChecks());
        obs.notif("PLOT AC");

      }
      if(event.getActionCommand() == "HIST"){
        System.out.println("Plot histogram!");
        selectionBounds = graphPanel.getSelectionBounds();
        obs.setBounds(selectionBounds[0],selectionBounds[1]);
        obs.setActiveChannels(checkPanel.getChecks());
        obs.notif("PLOT HIST");

      }
      if(event.getActionCommand() == "SIG"){
        System.out.println("Plot signal!");
        selectionBounds = graphPanel.getSelectionBounds();
        obs.setBounds(selectionBounds[0],selectionBounds[1]);
        obs.setActiveChannels(checkPanel.getChecks());
        obs.notif("PLOT SIG");

      }


      if(event.getActionCommand() == "STD"){
        System.out.println("Calculate standard deviation!");
        selectionBounds = graphPanel.getSelectionBounds();
        obs.setBounds(selectionBounds[0],selectionBounds[1]);
        obs.setActiveChannels(checkPanel.getChecks());
        obs.notif("CALC STD");

      }
      if(event.getActionCommand() == "ENTROP"){
        System.out.println("Calculate entropy!");
        selectionBounds = graphPanel.getSelectionBounds();
        obs.setBounds(selectionBounds[0],selectionBounds[1]);
        obs.setActiveChannels(checkPanel.getChecks());
        obs.notif("CALC ENTROP");

      }
      if(event.getActionCommand() == "CHECK"){
        System.out.println("CHECKBOX");
        graphPanel.drawGraphs(checkPanel.getChecks());
        repaint();
        setFocusable(true);
        requestFocusInWindow();

        //System.out.println()
      }
    }
    public void setObserver(Observer o){
      obs = o;
    }
    public void setProjectManager(ProjectManager proj){
      projObj = proj;
    }

  }



  private class ArrowListener extends KeyAdapter{
    public void keyPressed(KeyEvent event){
      if(event.getKeyCode()==38){
        Graph.zoom_multiplier *= 2;
        repaint();
        System.out.println("UPP");

      }
      if(event.getKeyCode()==40){
        if(Graph.zoom_multiplier > 1){
          Graph.zoom_multiplier /= 2;
          repaint();
        }
        System.out.println("DOWNN");
      }

    }
  }

}
