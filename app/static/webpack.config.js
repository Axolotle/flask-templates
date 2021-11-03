const path = require('path')
const webpack = require('webpack')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")

const dev = (process.env.NODE_ENV !== 'production')
const hashType = '[name]'
const root = path.resolve(__dirname)
const dist = path.resolve(__dirname, '..', 'dist')

module.exports = {
  mode: dev ? 'development' : 'production',
  devtool: 'source-map',

  entry: {
    app: [
      path.resolve(root, 'js', 'client.js'),
      path.resolve(root, 'scss', 'client.scss'),
    ],
    admin: [
      path.resolve(root, 'js', 'admin.js'),
      path.resolve(root, 'scss', 'admin.scss'),
    ]
  },

  output: {
    path: dist,
    filename: `js/${hashType}.js`,
    chunkFilename: `js/${hashType}.js`,
  },

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        },
      },
      {
        test: /\.scss$/,
        use: [
          dev ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['autoprefixer'],
              },
            },
          },
          'resolve-url-loader',
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
            },
          },
        ],
      },
      {
        test: /\.(eot|ttf|woff|woff2)$/,
        loader: 'file-loader',
        options: {
          name: `fonts/${hashType}.[ext]`,
        },
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        loader: 'file-loader',
        options: {
          name: `${hashType}.[ext]`,
          outputPath: (url, resourcePath, context) => {
            if (/node_modules/.test(resourcePath)) {
              return `vendors-imgs/${url}`
            }
            const basePath = path.relative(root, path.dirname(resourcePath))
            return `${basePath}/${url}`
          },
        },
      },
    ],
  },

  plugins: [new MiniCssExtractPlugin()],

  optimization: {
    splitChunks: {
      cacheGroups: {
        default: false,
        vendors: {
          name: 'vendors',
          test: /[\\/]node_modules[\\/]/,
          priority: -10,
          chunks: 'initial',
        },
      },
    },
  },

  devServer: {
    watchOptions: {
      ignored: /node_modules/,
    },
  },

  resolve: {
    extensions: ['.js'],
    alias: {
      '@': root,
    },
  },
}
