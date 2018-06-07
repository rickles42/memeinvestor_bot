# u/MemeInvestor_bot Documentation

## Contents

- [Welcome to meme investment!](#welcome-to-meme-investment)
- [Contributing](#contributing)
- [Investment behaviour](#investment-behaviour)
- [Commands](#commands)
- [Getting started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation and configuration](#installation-and-configuration)
- [Deployment](#deployment)
- [Source code](#source-code)
- [Authors](#authors)
- [License](#license)

## Welcome to meme investment!

Welcome to the source code repository of [u/MemeInvestor_bot](https://www.reddit.com/user/MemeInvestor_bot). 
This bot has been developed exclusively for [r/MemeEconomy](https://reddit.com/r/MemeEconomy/). It allows users
to create investment accounts with fictional MemeCoins, invest those MemeCoins in specific memes, and automatically
evaluate meme performance resulting in positive or negative returns.

## Contributing

If you want to contribute, please do so! Check the [Issues](https://github.com/MemeInvestor/memeinvestor_bot/issues) list and help meme investments thrive!

## Investment behaviour

To calculate the investment return, the bot performs a two-step procedure.

### First step

The bot calculates an initial growth factor, `y`, using a power function of the form `y = x^m`,
where `m` is a constant (`m=1/3`) and `x` is the relative change in
upvotes on the post since the investment was made as a proportion of the upvotes 
at the time of investment:  
`x=1+(final_upvotes - initial_upvotes)/initial_upvotes`.  
The 1/3 power function (cube root) behaviour was chosen so that the overall behavior
of the investment return function is a steep rise which levels off at higher upvote
growth. The reasoning behind this is to prevent a small handful of investors who get lucky
and invest in one or more posts that 'blow up' from earning so many MemeCoins that they
dominate the market from then on. This helps keep the playing field somewhat more
level for new investors. 
  
![Investment Return Initial Growth Factor](./data/investment_return_multiplier.png)
*Investment Return Initial Growth Factor*

### Second step

Unlike real stocks, reddit post upvotes typically either grow or don't grow; posts
don't usually get mass-downvoted by an appreciable amount and if they do, they quickly 
get buried, reducing the potential for downvoting. In light of this, so that investments aren't
risk-free, a graduated threshold is applied to the the factor calculated by the power function in the
first step. If the post grows such that this factor `y` is above the success threshold, `thresh = 1.2`,
the investment return is simply `invested_amount * y`. If the post grows (`y>1`) but the factor is at or
below 1.2, the investor only gets back `invested_amount * (y-1)/(thresh - 1)`. If the post doesn't grow
or is downvoted (`y<=1`), the investor gets back nothing.

![Investment Return Final Return Multiplier](./data/investment_return_multiplier_thresholding.png)
*Investment Return Final Return Multiplier vs Initial Growth Factor*

*Note:* The investment behaviour has already been through several design iterations
and may well be revised again in the future.

## Commands

The bot has the following commands:

- `!create` - creates a bank account for you with a new balance of 1000
  MemeCoins.
- `!invest AMOUNT` - invests AMOUNT in the meme (post). 4 hours after the
  investment, the meme growth will be evaluated and your investment can profit
  you or make you bankrupt. Minimum possible investment is 100 MemeCoins.
- `!balance` - returns your current balance.
- `!active` - returns a number of active investments.
- `!broke` - only if your balance is less than 100 MemeCoins and you do not have
  any active investments, declares bankruptcy on your account and sets your
  balance to 100 MemeCoins (minimum possible investment). 
- `!market` - gives an overview for the whole Meme market.
- `!top` - gives a list of the users with the largest account balances.
- `!ignore` - ignores the whole message.
- `!help` - returns this help message.

To invoke a command, reply to either the top-level u/MemeInvestor_bot comment in the comment section of any
r/MemeEconomy post or to one of its subsequent replies to your command comment.

## Getting started 

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes.

### Prerequisites

In order to run this application, you need to install [Docker](https://www.docker.com/community-edition).

### Configuration

The only thing that needs to be done before execution is the config profile. For that please follow the
steps below:

```
git clone https://github.com/thecsw/memeinvestor_bot
cd memeinvestor_bot
cp .env.example .env
nano .env
```

After filling out the details, save and exit. You're done with configuration.

### Deployment

From the root of the project directory, use `docker-compose up` to build and launch the various components
of the bot, including an empty database of investor accounts, the agents that monitor Reddit for new
submissions and commands, and the informational website.

It is time to make a fortune!

## Authors

 - *Sagindyk Urazayev* - Initial work and SQL Rewrite - [thecsw](https://github.com/thecsw)
 - *jimbobur* - Heavy additions to investment logic - [jimbobur](https://github.com/jimbobur)
 - *ggppjj* - Minor fixes - [ggppjj](https://github.com/ggppjj)
 - *rickles42* - Minor fixes and features - [rickles42](https://github.com/rickles42)
 - *TwinProduction* - Minor fixes and improvements - [TwinProduction](https://github.com/TwinProduction)

## License

This project is licensed under the The GNU General Public License (see the
[LICENSE.md](https://github.com/thecsw/prequelmemes_bot/blob/master/LICENSE) file for details), it explains everything pretty well. 
