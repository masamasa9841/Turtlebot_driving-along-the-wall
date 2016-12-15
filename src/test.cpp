#include <ros/ros.h>
#include <std_msgs/Float64.h>
#include <sensor_msgs/image_encodings.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
 
#define WIDTH   10
#define HEIGHT  25
#define WIDTH2   100
#define HEIGHT2  100
 
class depth_estimater{
public:
    depth_estimater();
    ~depth_estimater();
    void depthImageCallback(const sensor_msgs::ImageConstPtr& msg);
 
private:
    ros::NodeHandle nh;
    ros::Subscriber sub_rgb, sub_depth;
    ros::Publisher pub;
    ros::Publisher pub2;
};
 
depth_estimater::depth_estimater(){
    sub_depth = nh.subscribe<sensor_msgs::Image>("/camera/depth/image", 1, &depth_estimater::depthImageCallback, this);
    pub = nh.advertise<std_msgs::Float64>("left", 1);
    pub2 = nh.advertise<std_msgs::Float64>("center", 1);
    ros::Rate loop_rate(1);
}
 
depth_estimater::~depth_estimater(){
}
 
void depth_estimater::depthImageCallback(const sensor_msgs::ImageConstPtr& msg){
 
    int x1, x2, y1, y2, x3, x4, y3, y4;
    int i, j, k;
    int width = WIDTH;
    int height = HEIGHT;
    int width2 = WIDTH2;
    int height2 = HEIGHT2;
    double sum = 0.0;
    double sum2 = 0.0;
    double ave;
    double ave2;

    std_msgs::Float64 left;
    std_msgs::Float64 center;
    cv_bridge::CvImagePtr cv_ptr;
 
    try{
        cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_32FC1);
    }catch (cv_bridge::Exception& ex){
        ROS_ERROR("error");
        exit(-1);
    }
 
    cv::Mat depth(cv_ptr->image.rows, cv_ptr->image.cols, CV_32FC1);
    cv::Mat img(cv_ptr->image.rows, cv_ptr->image.cols, CV_8UC1);
 
    x1 = 0;
    x2 = width;
    y1 = int(depth.rows / 2) - height;
    y2 = int(depth.rows / 2) + height;
    
    x3 = int(depth.cols / 2) - width2;
    x4 = int(depth.cols / 2) + width2;
    y3 = int(depth.rows / 2) - height2;
    y4 = int(depth.rows / 2) + height2;
 
    for(i = 0; i < cv_ptr->image.rows;i++){
        float* Dimage = cv_ptr->image.ptr<float>(i);
        float* Iimage = depth.ptr<float>(i);
        char* Ivimage = img.ptr<char>(i);
        for(j = 0 ; j < cv_ptr->image.cols; j++){
            if(Dimage[j] > 0.0){
                Iimage[j] = Dimage[j];
                Ivimage[j] = (char)(255*(Dimage[j]/5.5));
            }else{
            }
 
            if(i > y1 && i < y2){
                if(j > x1 && j < x2){
                    if(Dimage[j] > 0.0){
                        sum += Dimage[j];
                    }
                }
            }
            if(i > y3 && i < y4){
                if(j > x3 && j < x4){
                    if(Dimage[j] > 0.0){
                        sum2 += Dimage[j];
                    }
                }
            }
        }
    }
 
    ave = sum / ((width * 2) * (height * 2));
    ave2 = sum2 / ((width2 * 2) * (height2 * 2));

    left.data = ave;
    center.data = ave2;
    pub.publish(left);
    pub2.publish(center);

    //ROS_INFO("left:%f[m] center:%f[m]", ave, ave2);
 
    //cv::imshow("DEPTH image", img);
    cv::waitKey(10);
}
 
int main(int argc, char **argv){
    ros::init(argc, argv, "depth_estimater");
 
    depth_estimater depth_estimater;
 
    ros::spin();
    return 0;
}
