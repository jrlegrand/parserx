const path = require( 'path' );
const HtmlWebPackPlugin = require("html-webpack-plugin");

module.exports = {
  context: __dirname,
  entry: './src/index.js',
  output: {
    path: path.resolve( __dirname, 'dist' ),
    filename: 'main.js',
    publicPath: '/',
  },
  devServer: {
    historyApiFallback: true
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: "html-loader"
          }
        ]
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.svg$/,
        use: [
          {
            loader: 'svg-url-loader',
            options: {
              limit: 10000,
            },
          },
        ],
      },

    ]
  },
  plugins: [
    new HtmlWebPackPlugin({
      template: path.resolve( __dirname, 'public/index.html' ),
      filename: "./index.html",
      favicon: path.resolve( __dirname, 'public/favicon.ico')
    })
  ],
  externals: {
    // global app config object
    config: JSON.stringify({
        apiUrl: 'https://api.parserx.io'
        //apiUrl: 'http://139.144.27.208'
        //apiUrl: 'http://192.168.1.20:8003'
        //apiUrl: 'http://192.168.1.14:8005'
    })
  }
};
