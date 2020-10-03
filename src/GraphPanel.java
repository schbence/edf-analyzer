import java.util.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.*;

public class GraphPanel extends JPanel {

  MovingAdapter ma = new MovingAdapter();
  ScaleHandler  sh = new ScaleHandler();
  private int selectFrom;
  private int selectTo;
  private int dataLength;
  private Observer observer;
  private float[][] data;
  private String[] chLabels;

  public GraphPanel(Observer obs, float[][] ys, String[] labels){

    addMouseMotionListener(ma);
    addMouseListener(ma);
    addMouseWheelListener(sh);

    observer = obs;
    data     = ys;
    chLabels = labels;
    //setVisible(true);
    //setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setPreferredSize(new Dimension(1044,600));
    setLayout(new GridLayout(0,1));
    dataLength = ys[0].length;
    setFocusable(true);
    requestFocusInWindow();


    //pack();
  }
  public void drawGraphs(boolean[] chVisible){
    removeAll();
    if(chVisible.length!=data.length){
      System.out.println("ERROR channel number and chVisible length do not match!");
    }
    for(int i=0;i<data.length;i++){
      Graph gr = new Graph(data[i],chLabels[i]);
      if(chVisible[i]==true){
        add(gr);
      }

    }
    setFocusable(true);
    requestFocusInWindow();
    revalidate();
    repaint();
  }

  public void reloadGraphs(float ys[][], String labels[]){
    data     = ys;
    chLabels = labels;
    dataLength = ys[0].length;
  }

  private class MovingAdapter extends MouseAdapter{
    private int x,y;
    public void mousePressed(MouseEvent e){
      if(Graph.view_x>0){
        if(e.getModifiers() == MouseEvent.BUTTON1_MASK){
          x = e.getX();
          y = e.getY();
        }
      }else{
        Graph.view_x=1;
      }
      if(e.getModifiers() == MouseEvent.BUTTON3_MASK){
        Graph.selFrom = e.getX();
        selectFrom = Graph.selFrom;
        repaint();
      }



    }
    public void mouseDragged(MouseEvent e){
      if(e.getModifiers() == MouseEvent.BUTTON1_MASK){
        int dx = e.getX() - x;
        int dy = e.getY() - y;
        if((Graph.view_x-dx*Graph.zoom_multiplier>0)&&(Graph.view_x+(Graph.view_width-dx)*Graph.zoom_multiplier<dataLength)){
          Graph.view_x-=dx*Graph.zoom_multiplier;
        }
        System.out.println(Graph.view_x);
        repaint();
        x+=dx;
      }

      if(e.getModifiers() == MouseEvent.BUTTON3_MASK){
        Graph.selTo = e.getX();
        selectTo = Graph.selTo;
        repaint();
      }

    }
  }

  private class ScaleHandler implements MouseWheelListener {
    public void mouseWheelMoved(MouseWheelEvent e){
      if (e.getScrollType() == MouseWheelEvent.WHEEL_UNIT_SCROLL){
        float amount = e.getWheelRotation();
        Graph.signalHeight += (int) amount*5;
        System.out.println(amount);
        repaint();
      }


    }
  }

  public int[] getSelectionBounds(){
    int[] sb = new int[2];
    sb[0] = Graph.view_x + Graph.zoom_multiplier * selectFrom;
    sb[1] = Graph.view_x + Graph.zoom_multiplier * selectTo;
    return sb;
  }
  public int[] getRelativeSelection(){
    int[] sel = new int[2];
    sel[0]    = selectFrom;
    sel[1]    = selectTo;
    return sel;
  }
  public int getZoomMultiplier(){
    return Graph.zoom_multiplier;
  }
  public void setZoomMultiplier(int newZoom){
    Graph.zoom_multiplier = newZoom;
  }

  public int getViewFrom(){
    return Graph.view_x;
  }
  public void setViewFrom(int newView){
    Graph.view_x = newView;
  }

  public int getSignalHeight(){
    return Graph.signalHeight;
  }
  public void setSignalHeight(int newHeight){
    Graph.signalHeight = newHeight;
  }



  public void setSelectionBounds(int from, int to){
    selectFrom = from;
    selectTo   = to;
    Graph.selFrom = selectFrom;
    Graph.selTo = selectTo;

    repaint();
  }


}
