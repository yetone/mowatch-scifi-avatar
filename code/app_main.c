/**
 * Sci-Fi HUD Watch Face
 * 科幻仪表盘风格表盘
 */

#include "header.h"
#include "avatar_graphics.h"
#include "background.h"
#include <string.h>

// 屏幕尺寸
#define SCREEN_W 200
#define SCREEN_H 200

// 头像位置 (中央上方)
#define AVATAR_CX 100
#define AVATAR_CY 60
#define AVATAR_SIZE 65

// 上次更新的分钟
static uint8_t last_min = 61;

// 星期
const char* week_str[] = {
    "SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"
};

/**
 * 绘制背景位图
 */
void draw_background(void) {
    int16_t i, j;
    int16_t byteWidth = (SCREEN_W + 7) / 8;

    for (j = 0; j < SCREEN_H; j++) {
        for (i = 0; i < SCREEN_W; i++) {
            if (background[j * byteWidth + i / 8] & (128 >> (i & 7))) {
                eink_drawpixel(i, j, BLACK);
            }
        }
    }
}

/**
 * 绘制缩放头像
 */
void draw_avatar(int cx, int cy, int display_size) {
    int16_t i, j;
    int16_t byteWidth = (120 + 7) / 8;
    int half = display_size / 2;
    int x = cx - half;
    int y = cy - half;

    int scale_num = 120;
    int scale_den = display_size;

    for (j = 0; j < display_size; j++) {
        for (i = 0; i < display_size; i++) {
            int src_x = (i * scale_num) / scale_den;
            int src_y = (j * scale_num) / scale_den;

            if (src_x < 120 && src_y < 120) {
                if (avatar_face[src_y * byteWidth + src_x / 8] & (128 >> (src_x & 7))) {
                    eink_drawpixel(x + i, y + j, BLACK);
                }
            }
        }
    }
}

/**
 * 绘制LED风格数字
 */
void draw_led_number(int x, int y, uint8_t num, uint16_t color) {
    if (num > 9) return;

    int16_t i, j;
    int16_t byteWidth = (NUM_WIDTH + 7) / 8;
    const unsigned char* bitmap = big_numbers[num];

    for (j = 0; j < NUM_HEIGHT; j++) {
        for (i = 0; i < NUM_WIDTH; i++) {
            if (bitmap[j * byteWidth + i / 8] & (128 >> (i & 7))) {
                eink_drawpixel(x + i, y + j, color);
            }
        }
    }
}

/**
 * 绘制LED冒号
 */
void draw_led_colon(int x, int y, uint16_t color) {
    eink_drawrect(x, y + 10, x + 5, y + 15, color, MODE_FILL);
    eink_drawrect(x, y + 18, x + 5, y + 23, color, MODE_FILL);
}

/**
 * 绘制时间 (中央大字)
 */
void draw_time(int center_x, int y) {
    uint8_t hour = RTC_getHour();
    uint8_t min = RTC_getMin();

    int digit_spacing = 3;
    int colon_width = 12;
    int total_width = NUM_WIDTH * 4 + digit_spacing * 3 + colon_width;
    int start_x = center_x - total_width / 2;

    // 小时
    draw_led_number(start_x, y, hour / 10, BLACK);
    start_x += NUM_WIDTH + digit_spacing;
    draw_led_number(start_x, y, hour % 10, BLACK);
    start_x += NUM_WIDTH + digit_spacing;

    // 冒号
    draw_led_colon(start_x, y, BLACK);
    start_x += colon_width;

    // 分钟
    draw_led_number(start_x, y, min / 10, BLACK);
    start_x += NUM_WIDTH + digit_spacing;
    draw_led_number(start_x, y, min % 10, BLACK);
}

/**
 * 绘制日期 (底部左侧面板)
 */
void draw_date(int x, int y) {
    char date_str[16];

    co_sprintf(date_str, "%d%d.%d%d",
        RTC_getMon() / 10, RTC_getMon() % 10,
        RTC_getDay() / 10, RTC_getDay() % 10);

    eink_drawstr(x, y, (const unsigned char*)date_str, 12, BLACK);

    // 星期
    eink_drawstr(x, y + 10, (const unsigned char*)week_str[RTC_getWeek()], 12, BLACK);
}

/**
 * 绘制电池指示 (底部右侧面板)
 */
void draw_battery(int x, int y) {
    uint8_t batt = watch_app_battpercent();
    char batt_str[8];
    int i;

    co_sprintf(batt_str, "%d%%", batt);
    eink_drawstr(x, y, (const unsigned char*)batt_str, 12, BLACK);

    // 电量条
    int bars = (batt * 6) / 100;
    for (i = 0; i < 6; i++) {
        int bx = x + i * 9;
        if (i < bars) {
            eink_drawrect(bx, y + 10, bx + 6, y + 14, BLACK, MODE_FILL);
        } else {
            eink_drawrect(bx, y + 10, bx + 6, y + 14, BLACK, MODE_EMPTY);
        }
    }
}

/**
 * 绘制科幻指标 - 辐射度 (左侧面板)
 */
void draw_radiation(int x, int y) {
    // 基于时间生成伪随机辐射值
    uint8_t hour = RTC_getHour();
    uint8_t min = RTC_getMin();
    int rad = ((hour * 17 + min * 3) % 100);
    char str[12];
    int i;

    // 标签
    eink_drawstr(x, y, (const unsigned char*)"RAD", 12, BLACK);

    // 数值
    co_sprintf(str, "%d.%d", rad / 10, rad % 10);
    eink_drawstr(x, y + 12, (const unsigned char*)str, 12, BLACK);

    // 单位
    eink_drawstr(x, y + 24, (const unsigned char*)"mSv", 12, BLACK);

    // 条形指示
    int level = rad / 20;  // 0-5
    for (i = 0; i < 5; i++) {
        int by = y + 38 + (4 - i) * 6;
        if (i < level) {
            eink_drawrect(x, by, x + 30, by + 4, BLACK, MODE_FILL);
        } else {
            eink_drawrect(x, by, x + 30, by + 4, BLACK, MODE_EMPTY);
        }
    }
}

/**
 * 绘制科幻指标 - 信号/系统状态 (右侧面板)
 */
void draw_system_status(int x, int y) {
    uint8_t sec = RTC_getSec();
    int signal = ((sec * 7) % 5) + 1;  // 1-5
    char str[12];
    int i;

    // 标签
    eink_drawstr(x, y, (const unsigned char*)"SYS", 12, BLACK);

    // 状态
    eink_drawstr(x, y + 12, (const unsigned char*)"NORM", 12, BLACK);

    // 信号强度
    eink_drawstr(x, y + 26, (const unsigned char*)"SIG", 12, BLACK);

    // 信号条
    for (i = 0; i < 5; i++) {
        int bx = x + i * 7;
        int h = 4 + i * 2;
        int by = y + 48 - h;
        if (i < signal) {
            eink_drawrect(bx, by, bx + 5, y + 48, BLACK, MODE_FILL);
        } else {
            eink_drawrect(bx, by, bx + 5, y + 48, BLACK, MODE_EMPTY);
        }
    }
}

/**
 * 绘制中央状态面板指标
 */
void draw_center_status(int x, int y) {
    uint8_t hour = RTC_getHour();
    uint8_t min = RTC_getMin();
    char str[16];

    // 坐标显示 (伪)
    int lat = 31 + (hour % 10);
    int lon = 121 + (min % 10);

    co_sprintf(str, "N%d E%d", lat, lon);
    eink_drawstr(x, y, (const unsigned char*)str, 12, BLACK);
}

/**
 * 绘制秒数指示器
 */
void draw_seconds_indicator(int x, int y, int w) {
    uint8_t sec = RTC_getSec();
    int progress = (sec * w) / 60;

    // 进度条背景
    eink_drawrect(x, y, x + w, y + 3, BLACK, MODE_EMPTY);
    // 进度
    if (progress > 0) {
        eink_drawrect(x, y, x + progress, y + 3, BLACK, MODE_FILL);
    }
}

/**
 * 绘制底部信息
 */
void draw_bottom_info(int y) {
    uint8_t hour = RTC_getHour();
    uint8_t min = RTC_getMin();
    char str[20];

    // 时间戳风格显示
    co_sprintf(str, "T+%d%d%d%d", hour/10, hour%10, min/10, min%10);
    eink_drawstr(70, y, (const unsigned char*)str, 12, BLACK);
}

/*
 * 界面更新函数
 */
void onDraw(void)
{
    eink_clear(WHITE);

    // 1. 绘制科幻背景
    draw_background();

    // 2. 绘制头像
    draw_avatar(AVATAR_CX, AVATAR_CY, AVATAR_SIZE);

    // 3. 左侧面板 - 辐射指标
    draw_radiation(10, 28);

    // 4. 右侧面板 - 系统状态
    draw_system_status(158, 28);

    // 5. 中央大时间
    draw_time(100, 106);

    // 6. 底部左 - 日期
    draw_date(12, 156);

    // 7. 底部中 - 状态/坐标
    draw_center_status(78, 156);

    // 8. 底部右 - 电量
    draw_battery(134, 156);

    // 9. 底部信息栏
    draw_bottom_info(182);

    // 10. 秒数进度条
    draw_seconds_indicator(20, 192, 160);
}

/*
 * 按键监听函数
 */
UpdateType onKey(ButtonType key)
{
    UpdateType update_flag = NONE_UPDATE;

#if SCREEN_TYPE == SCREEN_TYPE_MONO
    switch(key)
    {
        case KEY_BACK:
            update_flag = PART_UPDATE;
            watch_app_exit();
            break;
        default:
            break;
    }
#else
    switch(key)
    {
        case KEY_CENTER:
        case KEY_BACK:
            update_flag = PART_UPDATE;
            watch_app_exit();
            break;
        default:
            update_flag = FULL_UPDATE;
            break;
    }
#endif
    return update_flag;
}

/*
 * 定时调用函数
 */
UpdateType onUpdate(int delta)
{
    UpdateType update_type = NONE_UPDATE;

    if (last_min != RTC_getMin() && RTC_getSec() == 0)
    {
#if SCREEN_TYPE == SCREEN_TYPE_MONO
        update_type = PART_UPDATE;
#else
        if (RTC_getMin() % 5 == 0)
        {
            update_type = FULL_UPDATE;
        }
        else
        {
            update_type = PART_UPDATE;
        }
#endif
        last_min = RTC_getMin();
    }

    return update_type;
}

/**
 * 初始化
 */
void init_my_params(void)
{
    set_update_interval(1000);
    srand(RTC_getTimeStamp());
    last_min = RTC_getMin();
}

/*
 * app初始化函数
 */
void app_init(intptr_t *draw_ptr_t, intptr_t *onkey_ptr_t, intptr_t *update_ptr_t, intptr_t* func_arr)
{
    __initialize_datas(func_arr);
    *draw_ptr_t = (intptr_t)onDraw;
    *onkey_ptr_t = (intptr_t)onKey;
    *update_ptr_t = (intptr_t)onUpdate;

    init_my_params();
}
