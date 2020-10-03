import java.awt.*;
import javax.swing.*;
import java.util.*;
import java.util.Arrays;
import java.awt.event.*;


public class Graph extends JPanel {
  private float[] ys;
  private int[] xs,ystopaint,visible;
  private float min,max;
  private String CHlabel;
  public static int view_width = 1024;
  public static int zoom_multiplier = 2;
  public static int view_x = view_width*zoom_multiplier/2;
  public static int signalHeight = 60;
  private static Selection sel;
  public static int selFrom = 1;
  public static int selTo = 1;



  public Graph(float[] yin,String label){
    ys = yin;
    min = ys[0];
    max = ys[0];
    CHlabel = label;
    for(int i=0;i<ys.length;i++){
      if(ys[i]<min){
        min = ys[i];
      }
      if(ys[i]>max){
        max = ys[i];
      }
    }
    ystopaint = scaleY(ys,signalHeight,(getHeight()-signalHeight)/2);
    visible = Arrays.copyOfRange(ystopaint,view_x,view_x+view_width*zoom_multiplier);
    System.out.println("Max: "+max+" Min: "+min);
    xs = makexs(visible.length);
  }
  public int getLen(){
    return xs.length;
  }

  public void paint(Graphics g) {
      //g.setColor(Color.white);
      sel = new Selection();
      sel.setGraphics(g);
      ystopaint = scaleY(ys,signalHeight,(getHeight()-signalHeight)/2);
      visible = Arrays.copyOfRange(ystopaint,view_x,view_x+view_width*zoom_multiplier);
      xs = makexs(visible.length);
      Color dark = new Color(45, 45, 54);
      Color light = new Color(200,200,250);
      g.setColor(light);
      g.fillRect(0,0,getWidth(),getHeight());
      g.setColor(dark);
      g.drawPolyline(xs, visible, xs.length);
      g.setFont(new Font("Arial",Font.BOLD,12));
      g.setColor(dark);
      g.drawString(CHlabel,30,25);
      sel.setFrom(selFrom);
      sel.setTo(selTo);
      sel.drawSelection();
  }



  private int[] makexs(int len){
    int[] xs = new int[len];
    float temp;
    for(int i=0; i<len; i++){
      temp = (float)i  / (float)zoom_multiplier;
      xs[i] = (int) temp +10;
    }
    return xs;
  }

  private int[] scaleY(float[] ys,int height,int offset){
    float u;
    int[] scaled = new int[ys.length];
    for(int i=0;i<ys.length;i++){
      u = ((ys[i]-min)/(max-min));
      scaled[i] = (int)(u*height + offset);
    }
    return scaled;
  }
  private class Selection{
    private Graphics gr;
    private int fromX = 0;
    private int toX = 0;

    public void Selection(){
    }
    public void setGraphics(Graphics g){
      this.gr = g;
    }
    public void drawSelection(){
      gr.setColor(new Color(125,125,200,125));
      if (fromX<toX){
        gr.fillRect(fromX,0,toX-fromX,600);
      }else{
        gr.fillRect(toX,0,fromX-toX,600);
      }

    }
    public void setFrom(int fr){
      fromX = fr;
    }
    public void setTo(int to){
      toX = to;
    }
  }



}
