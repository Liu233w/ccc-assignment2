// ['entertainment', 'business', 'technology', 'gaming', 'music', 'sports', 'politics', 'fashion', 'health', 'food']
// ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#009688']

const topicColor = {
    'entertainment': '#5470c6',
    'business': '#91cc75',
    'technology': '#fac858',
    'gaming': '#ee6666',
    'music': '#73c0de',
    'sports': '#3ba272',
    'politics': '#fc8452',
    'fashion': '#9a60b4',
    'health': '#ea7ccc',
    'food': '#795548'
}

export default function getColorByTopic (topic) {
    return topicColor[topic]

}